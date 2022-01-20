class ApiError(Exception):
    def __init__(self, status_code=None, code=None, message=None):
        self.status_code = status_code
        self.message = message

        if code is None:
            if self.status_code is None:
                self.code = 400
            else:
                self.code = self.status_code
        else:
            self.code = code

        self.codes = {
            "100": "Continue",
            "101": "Switching Protocols",
            "102": "Processing",
            "103-199": "Unassigned",
            "200": "OK",
            "201": "Created",
            "202": "Accepted",
            "203": "Non-Authoritative Information",
            "204": "No Content",
            "205": "Reset Content",
            "206": "Partial Content",
            "207": "Multi-Status",
            "208": "Already Reported",
            "209-225": "Unassigned",
            "226": "IM Used",
            "227-299": "Unassigned",
            "300": "Multiple Choices",
            "301": "Moved Permanently",
            "302": "Found",
            "303": "See Other",
            "304": "Not Modified",
            "305": "Use Proxy",
            "306": "(Unused)",
            "307": "Temporary Redirect",
            "308": "Permanent Redirect",
            "309-399": "Unassigned",
            "400": "Bad Request",
            "401": "Unauthorized",
            "402": "Payment Required",
            "403": "Forbidden",
            "404": "Not Found",
            "405": "Method Not Allowed",
            "406": "Not Acceptable",
            "407": "Proxy Authentication Required",
            "408": "Request Timeout",
            "409": "Conflict",
            "410": "Gone",
            "411": "Length Required",
            "412": "Precondition Failed",
            "413": "Payload Too Large",
            "414": "URI Too Long",
            "415": "Unsupported Media Type",
            "416": "Range Not Satisfiable",
            "417": "Expectation Failed",
            "418-420": "Unassigned",
            "421": "Misdirected Request",
            "422": "Unprocessable Entity",
            "423": "Locked",
            "424": "Failed Dependency",
            "425": "Unassigned",
            "426": "Upgrade Required",
            "427": "Unassigned",
            "428": "Precondition Required",
            "429": "Too Many Requests",
            "430": "Unassigned",
            "431": "Request Header Fields Too Large",
            "432-499": "Unassigned",
            "500": "Internal Server Error",
            "501": "Not Implemented",
            "502": "Bad Gateway",
            "503": "Service Unavailable",
            "504": "Gateway Timeout",
            "505": "HTTP Version Not Supported",
            "506": "Variant Also Negotiates",
            "507": "Insufficient Storage",
            "508": "Loop Detected",
            "509": "Unassigned",
            "510": "Not Extended",
            "511": "Network Authentication Required",
            "512-599": "Unassigned"}

        if self.message is None:
            if str(self.code) not in self.codes:
                self.message = 'UNDEFINED'
            else:
                self.message = self.codes[str(self.code)]

        self.error = {
            'code': self.code,
            'message': self.message
        }

    def __str__(self):
        return repr(self.error)

    def to_dict(self):
        return {'code': self.code, 'message': self.message}