var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    getData(res);
});

function getData(res) {
    var mysql = require('mysql');

    var con = mysql.createConnection({
        host: "35.192.11.178",
        user: "root",
        password: "guBpJ1k33LNH9gdr",
        database: "iot_project"
    });


    con.connect(function(err) {
        if (err) throw err;
        if (err) throw err;
        con.query('SELECT * FROM iot_data', function(err, result, fields) {
            if (err) throw err;
            var table = "";
            table += '<table class="blueTable">';
            table +="<tr>";
            for(var column in result[0]){
                table += "<td><label> " + column + " </label></td>";
            }
            table +="</tr>";
            for(var row in result){
                table +="<tr>";
                for(var column in result[row]){
                    table +="<td><label> " + result[row][column] + " </label></td>";
                }
                table +="</tr>";
            }
            table +="</table>";
            res.render('index', { title: 'IOT Data' , data: table});
            con.end();
        });
    });

}

module.exports = router;
