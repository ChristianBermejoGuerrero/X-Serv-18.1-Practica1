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

    def parse(self, request):
        """Return the resource name (including /)"""

        recurso = request.split(' ',3)[1]    #nos quedamos con el recurso con la barra
        urlLong = None
        if request.split()[0] == "POST":
            method = "POST"
            urlLong = request.split('\r\n\r\n')[1][4:] #de este modo quitamos url=
            print(urlLong)
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

        if method != None:
            print("METODO: " + method)
        if resource != None:
            print("RESOURCE: " + resource)
        if urlLong != None:
            print("URLLONG: " + urlLong)

        # RECIBIMOS GET
        if method == "GET":
            if resource == "/":
                httpCode = "200 OK"
                htmlBody = "<html><body> Introduce una URL que desees acortar" \
                     + "<br><form method='POST' action=''>Contenido: <input type='text' name='url'><br>" \
                     + "<input type='submit' value='Enviar'></form></body></html>"

            else:
                resource = resource[1:]
                print("new resource: " + resource)
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
                #http%3A%2F%2F tenemos que adecuarlo a http://
                if urllib.parse.unquote(urlLong[0:13]) == strhttp:
                    urlLong = strhttp + urlLong[13:]
                elif urllib.parse.unquote(urlLong[0:14]) == "https://":
                    urlLong = "https://" + urlLong[14:]
                else:
                    urlLong = "http://" + urlLong #si viene sin http o https
# ****************************************************************************************************************************
                if urlLong in self.diccLong:     #si la URL a acortar esta ya en diccionario ARREGLAR SALIDAAAAAAAAAAAAAAAAAAA
                    print (urlLong + " YA ESTA EN EL DICCIONARIO")
                    urlShort = self.diccLong[urlLong]
                else:                           #si hay urlLong pero no esta en diccionario
                        self.diccLong[urlLong] = self.counter
                        print("CONTADOR: " + str(self.counter) + " URLsinacortar = " + urlLong)
                        self.diccShort[self.counter] = urlLong

                httpCode = "200 OK"
                htmlBody = "<html><body><a href=" + urlLong + ">" + "URL sin acortar" + "</a></p></body></html>" \
                            + "<html><body><a href=" + "'http://localhost:1234/'" + str(self.counter) \
                            + ">http://localhost:1234/" + str(self.counter) + "</a></p></body></html>"
                self.counter = self.counter + 1
        else:
            httpCode = "405 Method Not Allowed" #A request method is not supported gor the requuested resource
            hmtlBody = "Metodo no permitido"
        return (httpCode, htmlBody)


if __name__ == "__main__":
        testWebApp = getshorterURLApp("localhost", 1234)
