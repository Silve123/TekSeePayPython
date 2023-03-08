import cgi
from http import HTTPStatus
from http.server import  BaseHTTPRequestHandler
import socket
from HTTPAPI.apiServerHandler import handleJson, handlePOSTServerRequest, handlerStatus, handleGETServerRequest


class MyBaseRequestHandler(BaseHTTPRequestHandler):
    """"""
    

    def do_GET(self):
        self.responseJson = ""
        requestPath = self.path
        print("\n"*2+requestPath)

        # check path first
        print("-"*80)
        print("Processing Path...")
        pathStatus = handleGETServerRequest.checkPath(requestPath)
        print(f"Path Response: {pathStatus}")
        userId = requestPath.split("/")[-1] if pathStatus != handlerStatus.DRIVERS_FOR_PASSANGER else requestPath.split("/")[1]
        if pathStatus != handlerStatus.NOT_FOUND:
            jsonParseAttempt = handleJson(pathStatus, requestPath, userId).getJson() 
            if(jsonParseAttempt != handlerStatus.NOT_FOUND):
                self.OK_Response(jsonParseAttempt)
                return super().finish()

            self.NOT_FOUND_Response()
        else:
            self.NOT_FOUND_Response()
        print("-"*80)
        return super().finish()


    def do_POST(self):
        if self.command == "POST":
            resultOne = cgi.parse_header(self.headers.as_string())
            resultOne = resultOne[0].split("\n")[-1]
            requestPath = self.path
            print("\n"*2+requestPath)

            # check request first
            print("-"*80)
            print("Processing Path...")
            pathStatus = handlePOSTServerRequest.checkPath(requestPath, resultOne)
            print(f"Path Response: {pathStatus}")
            if pathStatus != handlerStatus.NOT_FOUND:
                jsonParseAttempt = handleJson(pathStatus, requestPath, requestPath.split("/")[2]).getJson() 
                if(jsonParseAttempt != None):
                    self.CREATED_Response(jsonParseAttempt)
                    return super().finish()
            else:
                self.NOT_CREATED_Response(jsonParseAttempt)
            print("-"*80)
       
        return super().finish()
    
    def OK_Response(self, JsonParse):
        self.send_response(HTTPStatus.OK)
        self.send_header("content-type", "json")
        self.end_headers()
        self.wfile.write(f"{JsonParse}".encode())

    def NOT_CREATED_Response(self, JsonParse):
        self.send_response(HTTPStatus.NOT_MODIFIED)
        self.send_header("content-type", "json")
        self.end_headers()
        self.wfile.write(f"{JsonParse}".encode())

    def CREATED_Response(self, JsonParse):
        self.send_response(HTTPStatus.CREATED)
        self.send_header("content-type", "json")
        self.end_headers()
        self.wfile.write(f"{JsonParse}".encode())

    def NOT_FOUND_Response(self):
        self.send_response(HTTPStatus.NOT_FOUND)
        self.send_header("content-type", "json")
        self.end_headers()
        self.wfile.write(f"{None}".encode())
    
    def handle_one_request(self) -> None:
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            mname = 'do_' + self.command
            if not hasattr(self, mname):
                self.send_error(
                    HTTPStatus.NOT_IMPLEMENTED,
                    "Unsupported method (%r)" % self.command)
                return
            method = getattr(self, mname)
            method()
            self.wfile.flush() #actually send the response if not already done.
        except ValueError:
            return
        except socket.timeout as e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
            return
        return super().handle_one_request()
    
   


