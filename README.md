# Mickey

Tiny personal script to grab stock buy/sell momentum data of Hong Kong stocks from [DB Power](http://www.dbpower.com.hk). Only Hong Kong stocks data are available.

## Getting Started

*Please note that it's a personal project. While I will try my best to show how to configure the script, there is a good chance some custom config isn't listed. Please start new issues for problem experieced. Thanks.*

The scripts has 2 parts:
1) Cron scripts to grab data from DBPower
2) Simple Flask web app to display data on local machine

### Prerequisites

- Python 3
- packages listed in *./requirements.txt*
- wget
- SQLite


### Installing

To install the crontab, please make sure the correct virtualenv path is included. Please refer to [this post](https://stackoverflow.com/questions/3287038/cron-and-virtualenv) for a proper setup.

Daily script is located at package root named *dailyscript.py*. However a shell script *daily.sh* is created along with it for a easier cron job setup. **Please make sure to edit the paths in *daily.sh* to get it work.**

Default daily webpage grab are stored in:
```
./mickey/powerticker/
```
with name *%Y%m%d.html*

Default SQLite database path is:
```
./master.db
```
Please edit in *config.py* to change it.

### Deployment

There are two config files for minimal Gunicorn + Ngnix setup for reference, they are located at:
```
./mickey/scripts/mickey_gunicorn.conf  # Gunicorn config
./mickey/scripts/mickey_nginx.conf  # Nginx config
``` 

### Others

Please note that *./weeklyscript.py* was never implemented. 

### Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Bootstrap](https://getbootstrap.com/) - HTML frontend library
* [SQLAlchemy](https://www.sqlalchemy.org/) - Database toolkit

## Contributing

Please read *CONTRIBUTING.md* for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/foongsy/mickey). 

## Authors

* **Henry Fong** - *Initial work* - [foongsy](https://github.com/foongsy)

See also the list of [contributors](https://github.com/foongsy/mickey/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
