# Mickey

Tiny personal script to grab data from [DB Power](http://www.dbpower.com). The data is considered useful to judge individual stock buy/sell momentum.

(Only Hong Kong stocks are provided)

## Getting Started

The scripts has 2 parts:
1) Cron scripts to grab data from DBPower
2) Simple Flask web app to display data on local machine

### Prerequisites

- Python 3
- packages listed in *requirements.txt*


### Installing

To install the crontab, please make sure the correct virtualenv path is included. Please refer to [this post](https://stackoverflow.com/questions/3287038/cron-and-virtualenv) for a proper setup.

Daily script is located at package root named *dailyscript.py*. However a shell script *daily.sh* is created along with it for a easier cron job setup.


Make sure change the path in *daily.sh* to your local path.
```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
