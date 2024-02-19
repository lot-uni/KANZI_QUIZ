$(document).ready(function() {
  $("#fetchData").click(function() {
      const url = location.href +"normal/";
      var context = document.getElementById("context").value;
      var title = document.getElementById("title").value;
      var quizSize = document.getElementById("quizSize").value;
      var level = document.getElementById("level").value;

      console.log(level);
      var data = {
        context: context,
        title: title,
        quizSize: quizSize,
        level: level
      }; // 送信するデータをオブジェクトとして作成
      $.ajax({
      type: "POST", // POSTリクエスト
      url: url, // サーバーのエンドポイントを指定
      crossDomain: true,
      xhrFields: {
        withCredentials: true // クレデンシャル情報を送信する
      },
      data: JSON.stringify(data), // データをJSON文字列に変換
      contentType: "application/json", // コンテンツタイプをJSONに指定
      dataType: "json", // レスポンスのデータタイプをJSONに指定
          success: function(data) {
              $("#DLC").css('display','initial');
              alert("問題がダウンロードできます");
              console.log("he")
          },
          error: function(xhr, status, error) {
            $("#result").text("Error: " + error);
            console.log("error")
          }
      });
  });
});
