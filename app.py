from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

EMAIL = "admin123"
PASSWORD = "user123"

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Health & Safety Training Portal</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #eef1f4;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            width: 900px;
            min-height: 520px;
            background: white;
            display: flex;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }

        .left {
            width: 50%;
            background: #172433;
            color: white;
            padding: 60px 45px;
        }

        .logo {
            width: 60px;
            height: 60px;
            background: #f28c28;
            border-radius: 8px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 25px;
        }

        h1 {
            font-size: 30px;
            line-height: 1.2;
            margin-bottom: 20px;
        }

        h1 span {
            color: #f28c28;
        }

        .left p {
            color: #d5dce3;
            line-height: 1.7;
            font-size: 15px;
        }

        .safety {
            margin-top: 35px;
            border-left: 4px solid #f28c28;
            padding-left: 15px;
        }

        .safety h3 {
            margin: 0 0 8px 0;
        }

        .safety p {
            font-size: 13px;
            margin: 0;
        }

        .right {
            width: 50%;
            padding: 60px 50px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .right h2 {
            color: #172433;
            font-size: 28px;
            margin: 0 0 8px 0;
        }

        .subtitle {
            color: #777;
            font-size: 14px;
            margin-bottom: 30px;
        }

        label {
            display: block;
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-bottom: 7px;
        }

        input {
            width: 100%;
            padding: 13px;
            border: 1px solid #ccc;
            border-radius: 6px;
            margin-bottom: 18px;
            font-size: 14px;
        }

        input:focus {
            outline: none;
            border-color: #f28c28;
        }

        button {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 6px;
            background: #f28c28;
            color: white;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #d97416;
        }

        .error {
            background: #ffe5e5;
            color: #c62828;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
            text-align: center;
            font-size: 13px;
        }

        .footer {
            text-align: center;
            margin-top: 25px;
            color: #999;
            font-size: 12px;
        }

        @media (max-width: 750px) {
            .container {
                width: 90%;
                flex-direction: column;
            }

            .left,
            .right {
                width: 100%;
            }
        }
    </style>
</head>

<body>

<div class="container">

    <div class="left">

        <div class="logo">LS</div>

        <h1>Logistics & <span>Safety</span></h1>

        <p>
            Health and Safety Training Portal for logistics,
            warehousing and automotive operations.
        </p>

        <div class="safety">
            <h3>Health & Safety First</h3>

            <p>
                Access training resources designed to promote
                safe working practices across logistics and
                warehouse environments.
            </p>
        </div>

    </div>

    <div class="right">

        <h2>Welcome Back</h2>

        <div class="subtitle">
            Sign in to access the training portal.
        </div>

        ERROR_MESSAGE

        <form method="POST">

            <label>Email</label>

            <input
                type="text"
                name="email"
                placeholder="Enter your email"
                required
            >

            <label>Password</label>

            <input
                type="password"
                name="password"
                placeholder="Enter your password"
                required
            >

            <button type="submit">
                SIGN IN
            </button>

        </form>

        <div class="footer">
            Health & Safety Training Programme
        </div>

    </div>

</div>

</body>
</html>
"""

SUCCESS_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Training Portal</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #eef1f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .box {
            background: white;
            padding: 50px;
            width: 500px;
            text-align: center;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }

        h1 {
            color: #172433;
        }

        p {
            color: #666;
        }

        .success {
            color: #2e7d32;
            font-weight: bold;
        }
    </style>
</head>

<body>

<div class="box">

    <h1>Login Successful</h1>

    <p class="success">
        Welcome to the Health & Safety Training Portal.
    </p>

    <p>
        You have successfully logged in.
    </p>

</div>

</body>
</html>
"""


class LoginHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        page = LOGIN_PAGE.replace("ERROR_MESSAGE", "")

        self.wfile.write(page.encode("utf-8"))

    def do_POST(self):

        length = int(self.headers.get("Content-Length", 0))

        data = self.rfile.read(length).decode("utf-8")

        form = parse_qs(data)

        email = form.get("email", [""])[0]
        password = form.get("password", [""])[0]

        if email == EMAIL and password == PASSWORD:

            page = SUCCESS_PAGE

        else:

            error = """
            <div class="error">
                Invalid email or password.
            </div>
            """

            page = LOGIN_PAGE.replace(
                "ERROR_MESSAGE",
                error
            )

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        self.wfile.write(page.encode("utf-8"))


server = HTTPServer(("localhost", 8000), LoginHandler)

print("")
print("========================================")
print(" Health & Safety Training Portal")
print("========================================")
print("")
print("Server running at:")
print("http://localhost:8000")
print("")
print("Email: admin123")
print("Password: user123")
print("")
print("Press CTRL+C to stop the server.")
print("")

server.serve_forever()