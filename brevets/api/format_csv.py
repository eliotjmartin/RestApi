import flask

def csv_form(db, k, all="all"):
    entries = db.tododb.find()
    if k <= 0 or k >=entries.count():
        k = entries.count()
    open = []
    close = []
    for i in entries:
        open.append(i['open'])
        close.append(i['close'])
    response = []
    open = open[0:k]
    close = close[0:k]
    if all == "all":
        response.append(["Open", "Close"])
        for i in range(len(open)):
            tmp = []
            tmp.append(open[i])
            tmp.append(close[i])
            response.append(tmp)
    if all == "open":
        response.append(["Open"])
        for i in range(len(open)):
            tmp = []
            tmp.append(open[i])
            response.append(tmp)
    if all == "close":
        response.append(["Close"])
        for i in range(len(close)):
            tmp = []
            tmp.append(close[i])
            response.append(tmp)
    for i in range(len(response)):
        response[i] = ",".join(response[i])
    return "\n".join([v for v in response])

def json_form(db, k, all="all"):
    entries = db.tododb.find()
    if k <= 0 or k >=entries.count():
        k = entries.count()
    open = []
    close = []
    for i in entries:
        open.append(i['open'])
        close.append(i['close'])
    open = open[0:k]
    close = close[0:k]
    response = {'Open':open, 'Close':close}
    if all == "open":
        del response['Close']
    if all == "close":
        del response['Open']
    return flask.jsonify(response)