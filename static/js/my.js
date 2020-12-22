

//------------------------------上传事件-------------------------------------

document.querySelector('#upload-button').onclick = () => {document.querySelector("#upload-file").click()};

document.querySelector("#upload-file").onchange = () => {

  let files=document.getElementById('upload-file').files;
  
  if (files.length ===0) return;
  
  let form = new FormData(),
    url = 'http://127.0.0.1:9584/upload/', //服务器上传地址
    file = files[0];
  form.append('file', file);

  var xhr = new XMLHttpRequest();
  xhr.withCredentials = true;
  
  xhr.open("POST", url, true);


  xhr.upload.addEventListener("progress", function(result) {
    if (result.lengthComputable) {
        //上传进度
        var percent = (result.loaded / result.total * 100).toFixed(2);
    }
  }, false);

  xhr.readystatechange =function() {
      let result = xhr;
      if (result.status != 200) { //error
          console.log('上传失败', result.status, result.statusText, result.response);
      }
      else if (result.readyState == 4) { //finished
          console.log('上传成功', result);
      }
  };
  xhr.send(form); //开始上传

};


