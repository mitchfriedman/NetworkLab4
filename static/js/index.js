$(document).ready(function() {
    
    function search(data) {
        $.ajax({
            url: "/api/Search/" + data,
            type: "GET",
            success: function(resp){
                $("#results").empty();
                console.log(resp.data);
                resp.data.forEach(function(article) {
                    console.log(article);
                    newDiv = "" +
                             "<h3>" + article.headline + "</h3>" + 
                             "<p>" + article.snippet + "</h3><hr>";
                    
                    $("#results").append(newDiv);
                });
            }
        });
    }
    
    $("#search-button").click(function(e) {
        var searchData = $("#search-text").val();
        search(searchData);
    });

    if (window.location.href.indexOf("static") > -1) {
        search("mock");
    }
});
