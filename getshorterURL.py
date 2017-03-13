#!/usr/bin/python3

#dado un recurso miramos en el diccionario que tenemos la clave que nos pasan y devolvemos a la página html su valor
"""
 contentApp class
 Simple web application for managing content

 Copyright Jesus M. Gonzalez-Barahona, Gregorio Robles 2009-2015
 jgb, grex @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - March 2015
"""

import webapp
import csv
import urllib.parse
import os


class getshorterURLApp (webapp.webApp):
    """Simple web application for managing content.

    Content is stored in a dictionary, which is intialized
    with the web content."""

    # Declare and initialize content
    diccLong = {}
    diccShort = {}
    counter = 0;
    httpCode = " "
    htmlBody = " "

    def saveURL(self,urlLong,urlShort):
        """ Save each URL into csv file (append)"""
        with open("data.csv", "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([int(urlShort)] + [urlLong])
        return None

    def readDicc(self,file):
        """ Read csv file to creat our dictionarys.
        The file 'data.csv' must be created before executing"""

        with open('data.csv', 'r') as csvfile:
            if os.stat('data.csv').st_size == 0: #si es igual a 0 el fichero esta vacio
                print("EL FICHERO ESTA VACIO")
            else:
                reader = csv.reader(csvfile)
                for row in reader: #siguiendo lo que hemos hecho, row[0] = urlshort y row[1] = urlLong
                    self.diccLong[row[1]] = int(row[0])
                    self.diccShort[int(row[0])] = row[1]
                    self.counter = self.counter + 1
        return None

    def parse(self, request):
        """Return the resource name (including /)"""

        recurso = request.split(' ',3)[1]    #nos quedamos con el recurso con la barra
        urlLong = None
        if request.split()[0] == "POST":
            method = "POST"
            urlLong = request.split('\r\n\r\n')[1][4:] #de este modo quitamos url=
        elif request.split()[0] == "GET":
            method = "GET"
        else: # recibo otra cosa que no sea POST o GET
            method = "ERROR"

        return(method,recurso,urlLong)

    def process(self, resourceName):        #resourceName es lo que antes llamabamos parsedRequest
        """Process the relevant elements of the request.

        Finds the HTML text corresponding to the resource name,
        ignoring requests for resources not in the dictionary.
        """
        global httpCode,htmlBody
        i = 0;
        strhttp = "http://"
        method, resource, urlLong = resourceName

        if len(self.diccLong) == 0: #inicializamos ambos diccionarios si no lo estan todavia leyendo filecsv
            self.readDicc("data.csv")
        # RECIBIMOS GET
        if method == "GET":
            if resource == "/":
                httpCode = "200 OK"
                htmlBody = "<html><body> Introduce una URL que desees acortar" \
                     + "<br><form method='POST' action=''>Contenido: <input type='text' name='url'><br>" \
                     + "<input type='submit' value='Enviar'></form></body></html>"

            else:
                resource = resource[1:]
                if str.isdigit(resource):
                    resource = int(resource)
                    if resource in self.diccShort:
                        # REDIRECCION A LA URL SIN ACORTAR QUE ESTE DEFINIDA POR resource
                        httpCode = "301"
                        htmlBody = "<html><meta http-equiv= 'Refresh'" \
                            + "content='0;url=" + self.diccShort[resource] + "'>"
                    else:
                        httpCode = "404 Not Found"
                        htmlBody = "<html><body> Recurso no disponible.</body></html>"
                else:
                    httpCode = "404 Not Found"
                    htmlBody = "<html><body> Introduce un numero valido.</body></html>"

        # RECIBIMOS POST
        elif method == "POST":
            if urlLong != None: #en el cuerpo del POST venia url=http...
                #http%3A%2F%2F contamos 13 con http y 14 con https, tenemos que adecuarlo a http://
                if urllib.parse.unquote(urlLong[0:13]) == strhttp:
                    urlLong = strhttp + urlLong[13:]
                elif urllib.parse.unquote(urlLong[0:14]) == "https://":
                    urlLong = "https://" + urlLong[14:]
                else:
                    urlLong = "http://" + urlLong #si viene sin http o https
                if urlLong in self.diccLong:     #si la URL a acortar esta ya en diccionario
                    print (urlLong + " YA ESTA EN EL DICCIONARIO")
                    urlShort = self.diccLong[urlLong]
                else:                           #si hay urlLong pero no esta en diccionario
                        self.diccLong[urlLong] = self.counter
                        self.diccShort[self.counter] = urlLong
                        urlShort = self.counter
                        self.saveURL(urlLong,urlShort)
                        self.counter = self.counter + 1

                httpCode = "200 OK"
                htmlBody = "<html><body>URL SIN ACORTAR: <a href=" + urlLong + ">" + urlLong + "</a></p></body></html>" \
                            + "<html><body>URL ACORTADA: <a href=" + "'http://localhost:1234/" + str(urlShort) \
                            + "'>" + str(urlShort) + "</a></p></body></html>"
        else:
            httpCode = "405 Method Not Allowed" #A request method is not supported gor the requuested resource
            hmtlBody = "Metodo no permitido"
        return (httpCode, htmlBody)


if __name__ == "__main__":
    try:
        testWebApp = getshorterURLApp("localhost", 1234)
    except KeyboardInterrupt:
        print ("\nClosing binded socket")
