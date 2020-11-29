function images_ajax(url, fun) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      fun(this.responseText);
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}

function images_show_lightbox(data, height = "300px", width = "400px") {
  var q = document.querySelector(".lightbox .data");
  var c = document.querySelector(".lightbox-content");
  q.style.height = height;
  q.style.width = width;
  q.innerHTML = data;
  document.querySelector(".lightbox").classList.add("opened");
}
/*
search_input;
fa - search;*/

function search(e) {
  if (e.keyCode === 13) {
    e.preventDefault();
    window.location.href =
      "/search/" + document.querySelector(".search_input").value + "/";
  }
}
function edit_mydata() {
  images_ajax("/edit_my_data", function (data) {
    images_show_lightbox(data, "450px", "450px");
  });
}

function add_image() {
  images_ajax("/addimage", function (data) {
    images_show_lightbox(data, "450px", "450px");
  });
}

function edit_image(id) {
  images_ajax("/editimage/" + id, function (data) {
    images_show_lightbox(data, "550px", "450px");
  });
}

function delete_image(id) {
  if (confirm("Are you sure you want to delete image ?")) {
    images_ajax("/deleteimage/" + id, function (data) {
      alert(data);
      window.location.reload();
    });
  }
}

function get_image(id) {
  images_ajax("/image/" + id, function (data) {
    images_show_lightbox(data, "600px", "800px");
  });
}
function like_image(e) {
  images_ajax(
    "/imagelike/" + e.dataset.image_id + "/" + e.dataset.user_id,
    function (res) {
      var p = e.parentNode;

      var para = document.createElement("span");
      para.innerHTML = res;
      console.log(para.children[0]);

      p.insertBefore(para.children[0], e);

      e.remove();
    }
  );
}

function follow_user(e) {
  images_ajax(
    "/follow/" + e.dataset.follow_id + "/" + e.dataset.user_id,
    function (res) {
      var p = e.parentNode;

      var para = document.createElement("span");
      para.innerHTML = res;
      console.log(para.children[0]);

      p.insertBefore(para.children[0], e);

      e.remove();
    }
  );
}
