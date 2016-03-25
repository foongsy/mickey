from mickey import app
from mickey import models
app.config.from_object('config')

app.run(host='0.0.0.0',port=5000,debug=True)
