// <script>
//   document.getElementById("getURL").innerHTML = window.location.href;
//   console.log("ok")
// </script>
<script>
// STORE PAGE
  var a = document.getElementById("getURL").value = window.location.href;
  console.log(a);
  function DuplicateURL() {
    var copyText = document.getElementById("getURL");
    copyText.select();
    document.execCommand("Copy");
    alert("Copied the URL: " + copyText.value);
  }

  $("#getURL").click(function(){
    $(this).select();
    document.execCommand("Copy");
  });

  var x = document.URL;
  // $("#test").html(x);
  // console.log($("#test").html(x));
  $("#fb").attr('href', 'https://www.facebook.com/sharer/sharer.php?u='+x);
  $("#gplus").attr('href', 'https://plus.google.com/share?url='+x);
  console.log($("#test").attr('href', 'https://plus.google.com/share?url='+ x));

  $(".like").click(function(){
    $(this).css('color', 'red');
  });

  $(".like").dblclick(function(){
    $(this).css('color', 'grey');
  });

</script>
