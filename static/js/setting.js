$(document).ready(function() {
  $("#fetchData").click(function() {
      const url = "http://127.0.0.1:8000/normal/";
      var context = document.getElementById("context").value;
      var title = document.getElementById("title").value;
      var quizSize = document.getElementById("quizSize").value;

      console.log(title);
      var data = {
        context: context,
        title: title,
        quizSize: quizSize
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
              alert("pdfの生成に成功しました。")
          },
          error: function(xhr, status, error) {
            $("#result").text("Error: " + error);
          }
      });
  });
});