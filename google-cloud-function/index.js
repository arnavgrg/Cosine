/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */
let request = require('request');
var apiresp;


function initialize(optns) {
    // Setting URL and headers for request
    var options = optns;
    // Return new promise 
    return new Promise(function(resolve, reject) {
    	// Do async job
        request.post(options, function(err, resp, body) {
            if (err) {
                reject(err);
            } else {
                resolve(JSON.parse(body));
            }
        })
    })
}

exports.getSentiment = (req, res) => {
  
  console.log('In the func');
  
  //let message = req.query.message || req.body.message || 'Hello World!';
  if(req.body.text) {
		let str = req.body.text;
    	let resul = str.split('\n\n');
        let sendtosenti = resul;
        // run senti on resul
       /* for(let i = 0; i < resul.length; i+=5) {
            let apme = "";
            if(i + 5 >= resul.length) {
                for(let j = i; j < resul.length; j++) {
                    apme = apme + resul[j] + ".";
                }
            }
            else {
                for(let j = i; j < i + 5; j++) {
                    apme = apme + resul[j] + ".";
                }
            }
            sendtosenti.push(apme.trim());
        }*/
        let details = [];
        for(let k = 0; k < sendtosenti.length; k++) {
          let jso = {
            'language': 'en',
            'id': k+1,
            'text': sendtosenti[k]
          };
          details.push(jso);
        }
    
  		var options = {
             method: 'POST',
             url: 'https://westus2.api.cognitive.microsoft.com/text/analytics/v2.1/sentiment',
             headers: {
                 'Accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Ocp-Apim-Subscription-Key': '91baa626ce1b41ffbe847be07e4a33fd' 
             },
             body: JSON.stringify({ 
               'documents': details
			 })
         };
    
    	var initializePromise = initialize(options);
        initializePromise.then(function(result) {
            apiresp = result;
            return apiresp;
        }, function(err) {
            console.log(err);
        }).then(function(result) {
           	let jos = result.documents;
          	let scores = 0;
          	for(let l = 0; l < jos.length; l++) {
				scores += jos[l].score;             	
             }
          	let avg = scores/jos.length;
           	let respo = {
           		"score": avg
            };
            res.setHeader('Access-Control-Allow-Methods', 'GET, POST')
            res.setHeader('Content-Type', 'application/json');
            res.setHeader('Access-Control-Allow-Origin', '*');
            res.status(200).send(respo);
        })
    }
    else {
          res.status(200).send("Please pass a name on the query string or in the request body");
    }
 };