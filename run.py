from mickey import app
from mickey import models
app.config.from_object('config')

app.run(host='127.0.0.1',port=5000,debug=True)
