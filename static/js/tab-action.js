// タブ
const tabList = document.querySelectorAll('.tab');
// タブコンテンツ
const tabContent = document.querySelectorAll('.tab-contents-item');

//DOMが読み込み終わったら
document.addEventListener('DOMContentLoaded', function(){
  // タブに対してクリックイベントを適用
  for(let i = 0; i < tabList.length; i++) {
    tabList[i].addEventListener('click', tabSwitch);
  }
  // タブをクリックすると実行する関数
  function tabSwitch(){
    // activeクラスを削除
    document.querySelectorAll('.active')[0].classList.remove('active');
    // クリックしたタブにactiveクラスを付与    
    this.classList.add('active');
    // showクラスを削除
    document.querySelectorAll('.show')[0].classList.remove('show');
    // タブを配列風オブジェクトとして定義
    const aryTabs = Array.prototype.slice.call(tabList);
    // クリックしたタブの配列番号を取得     
    const index = aryTabs.indexOf(this);
    // クリックしたタブと同じ配列番号のタブコンテンツにshowクラスを付与    
    tabContent[index].classList.add('show');
  };
});