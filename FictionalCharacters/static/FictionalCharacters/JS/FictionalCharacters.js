  writeRandomQuote = function() {
    var quotes = new Array();
    quotes[0] = new Image();
    quotes[0].src = '/static/FictionalCharacters/images/Characters_hannibal.png';
    quotes[1] = new Image();
    quotes[1].src = '/static/FictionalCharacters/images/Characters_janeway.png';
    quotes[2] = new Image();
    quotes[2].src = '/static/FictionalCharacters/images/Characters_magua.png';
    quotes[3] = new Image();
    quotes[3].src = '/static/FictionalCharacters/images/Characters_scully.png';
    var rand = Math.floor(Math.random()*quotes.length);
    document.getElementById("fcquote").appendChild(quotes[rand]);
  }
  writeRandomQuote();
