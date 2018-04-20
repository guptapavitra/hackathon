const rp = require('request-promise');
const cheerio = require('cheerio');
const chalk = require('chalk').default;

var fs = require('fs');
var parse = require('csv-parse');

var csvData = [];

fs.createReadStream("hackathon.csv")
    .pipe(parse({
        delimiter: ','
    }))
    .on('data', function (csvrow) {
        var url = csvrow[1];
        if (url && url.length < 100) {
            return;
        }
        console.log(chalk.bgBlue(url));
        getScrapedData("https://" + url);
    })
    .on('end', function () {
        //do something wiht csvData
        console.log(csvData);
    });



function getScrapedData(url) {
    const options = {
        uri: url,
        transform: function (body) {
            return cheerio.load(body);
        }
    };

    rp(options).then(function ($) {
        console.log('SUCCESS!')
        var heading = $('article h1').text();
        var data = $('article .data').text();
        var date = $('article .dt').text();

        if (!data || !date || !heading) {
            return;
        }

        setScrapedData(formatData(url), formatData(heading), formatData(data), formatData(date));
    }).catch(function (err) {
        console.log(err);
    });
}

function formatData(data) {
    return  data.replace(/(\r\n\t|\n|\r\t)/gm, " ");
}

function setScrapedData() {
    var finalData = Array.from(arguments).join("|") + "\n";

    fs.appendFile("scraped-data.csv", finalData, function(err) {
        if(err) {
            return console.log(err);
        }
    
        console.log("Done!!!");
    });
}