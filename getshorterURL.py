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



class contentApp (webapp.webApp):
    """Simple web application for managing content.

    Content is stored in a dictionary, which is intialized
    with the web content."""

    # Declare and initialize content
    content = {}
    contentReverse = {}
    httpCode = " "
    htmlBody = " "

    def parse(self, request):
        """Return the resource name (including /)"""

        recurso = request.split(' ',3)[1]    #nos quedamos con el recurso con la barra
        urlLong = None
        if request.split()[0] == "POST":
            method = "POST"
            urlLong = request.split('\r\n\r\n')[1][4:] #de este modo
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
        method, resource, urlLong = resourceName
        if method != None:
            print("METODO: " + method)
        if resource != None:
            print("RESOURCE: " + resource)
        if urlLong != None:
            print("URLLONG: " + urlLong)
        strhttp = "http://"

        # RECIBIMOS GET
        if method == "GET":
            if resource == "/":
                httpCode = "200 OK"
                htmlBody = "<html><body> Introduce una URL que desees acortar" \
                     + "<br><form method='POST' action=''>Contenido: <input type='text' name='url'><br>" \
                     + "<input type='submit' value='Enviar'></form></body></html>"

            else:
                resource = resource[1:]
                print("nuevo resource: " + resource)
                if str.isdigit(resource):
                    if resource in self.contentReverse:
                        # REDIRECCION A LA URL SIN ACORTAR QUE ESTE DEFINIDA POR resource
                        httpCode = "301"
                        htmlBody = "<html><meta http-equiv= 'Refresh'" \
                            + "content='0;url=" + self.contentReverse[resource] + "'>"
                    else:
                        httpCode = "404 Not Found"
                        htmlBody = "<html><body> Recurso no disponible.</body></html>"
                else:
                    httpCode = "404 Not Found"
                    htmlBody = "<html><body> Introduce un numero valido.</body></html>"

        elif method == "POST":
            # RECIBIMOS POST
            print(urlLong)
            if urlLong in self.content:     #si el nombre del recurso esta en diccionario
                print("POSTTTTTTTTTTT111111")
                httpCode = "200 OK"         #quiere decir que ya hemos acortado esa URL y devolvemos la url acortada
                htmlBody = "<html><body>" + self.content[urlLong] \
                    + "</body></html>"
            else:                           #si hay urlLong pero no esta en diccionario
                if urlLong.find(strhttp,0,7) != -1: #si empieza por http://
                    print("POSTTTTTTTTTTT222222222222")
                    self.content[urlLong] = i
                    self.contentReverse[i] = urlLong
                    i = i + 1
                    httpCode = "200 OK"
                    htmlBody = "<html><body><a href=" + urlLong + ">" + urlLong + "</a></p></body></html>" \
                        + "<html><body><a href=" + "'http://localhost:1234/'" + str(i) + ">http://localhost:1234/" + str(i) + "</a></p></body></html>"
                else:
                    print("POSTTTTTTTTTTT33333333")
                    urlLong = strhttp + urlLong
                    self.content[urlLong] = i
                    self.contentReverse[i] = urlLong
                    httpCode = "200 OK"
                    htmlBody = "<html><body><a href=" + urlLong + ">" + urlLong + "</a></p></body></html>" \
                        + "<html><body><a href=" + "'http://localhost:1234/'" + str(i) + ">http://localhost:1234/" + str(i) + "</a></p></body></html>"
                    i = i + 1
        else:
            httpCode = "405 Method Not Allowed" #A request method is not supported gor the requuested resource
            hmtlBody = "Metodo no permitido"
        return (httpCode, htmlBody)


if __name__ == "__main__":
        testWebApp = contentApp("localhost", 1234)
