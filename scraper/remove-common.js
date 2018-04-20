var fs = require("fs");

var oneUrls = getUrls('scraped-data-1.csv');
var twoUrls = getUrls('scraped-data-2.csv');

function getUrls(path) {
    var two = fs.readFileSync(path, 'utf8');

    var twoRows = two.split("\n");
    var twoUrls = [];

    twoRows.forEach(function (twoRow) {
        var twoSplittedRow = twoRow.split("|");
        twoSplittedRow && twoUrls.push(twoSplittedRow[0]);
    });

    return twoUrls;
}

twoUrls.forEach(function (twoUrl) {
    if (oneUrls.includes(twoUrl)) {
        console.log(twoUrl);
        return;
    }

    // fs.appendFile('', 'wtf', (err) => {
    //     if (err) throw err;
    //     console.log('The "data to append" was appended to file!');
    // });
});