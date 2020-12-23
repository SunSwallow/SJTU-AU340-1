

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



// ------------------------------------加载图表----------------------------------------------
var chart = echarts.init(document.getElementById('chart'), 'dark', {renderer: 'canvas'});
chart.showLoading();
const myRequest = new Request("http://127.0.0.1:9584/data");

var allData = null;


fetch(myRequest)
    // .then(chart.hideLoading();)
    .then(re => re.json())// 获取json文件
    .then(process_add_button) // 处理数据 添加按钮
    .then(data => get_opt(data)) // 获取opt
    .then(opt => {chart.hideLoading();chart.setOption(opt);}) // 绘图
    .then(add_event) // 为每一个button添加触发事件


// 处理返回的json数据，添加Yawing按钮
function process_add_button(data){
    let yawing = document.getElementById('yawing');
    if (yawing !== null){yawing.parentNode.removeChild(yawing);}
    yawing = document.createElement("ul");
    yawing.id = 'yawing';
    let count = 0;
    // let num = Object.keys(data).length;
    // let width = window.getComputedStyle(document.getElementById('pic')).width / num;
    
    for (let ele in data) {
        button = document.createElement("button");
        button.classList.add("y");
        // button.style.width = width;
        button.innerText = 'Yawing'+String(count);
        if ( Object.keys(data)[count].indexOf('bad') !== -1){
            button.value = 'bad';
        } else {
            button.value = 'good';
        }
        count++;
        let list = document.createElement("li");
        list.appendChild(button)
        yawing.appendChild(list);
    };
    document.querySelector('.mainbox').insertBefore(yawing,document.getElementById('pic'));
    allData = data;
    return data[Object.keys(data)[0]];
}

function flash_chart(e) {
    console.log("Clicking here：",e.target)
    index = Number(e.target.innerText[e.target.innerText.length-1]);
    chart.setOption(get_opt(allData[Object.keys(allData)[index]]));
}


function add_event(){ 
    console.log('add event')
    buttons = document.querySelectorAll('#yawing button');
    for (i=0;i< buttons.length;i++){
        everyButton = buttons[i]
        console.log("adding on",everyButton.innerText)
        everyButton.onclick = flash_chart;
    }
}


// 指定图表的配置项和数据
function get_opt(metadata) {
    console.log(metadata)
    var option = {
        title: {
            text: '发电机工作参数',
            subtext: '',
            left: 'center',
            textStyle: {
                fontSize: 28,
                fontWeight: 'bolder',
                color: '#333',      // 主标题文字颜色
                textStyle:'Microsoft YaHei',
            },
        },
        
        tooltip: {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'cross'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },

        toolbox: {
            show: true,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                dataView: {readOnly: false},
                restore: {},
                saveAsImage: {}
            }
        },

        legend: {
            type :'scroll',
            orient: 'vertical',
            x: 'right', 
            y: 'middle',
            data: [
                'Axis0Torque',
                'Axis1Torque',
                'Axis2Torque',
                'Axis3Torque',
                'Axis4Torque',
                'Axis0Velocity',
                'Axis1Velocity',
                'Axis2Velocity',
                'Axis3Velocity',
                'Axis4Velocity',
                        ]
        },

        dataZoom: [{
            type: 'inside',
            xAxisIndex: [0,1],
            start: 0,
            end: 100
        }, {
            start: 0,
            end: 100,
            xAxisIndex: [0,1],
            handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
            handleSize: '80%',
            handleStyle: {
                color: '#fff',
                shadowBlur: 3,
                shadowColor: 'rgba(0, 0, 0, 0.6)',
                shadowOffsetX: 2,
                shadowOffsetY: 2
            }
        }],

        grid: [{  // 布局
            left: 100,
            right: 400,
            top: 80,
            height: 500
        }, {
            left: 100,
            right: 400,
            bottom: 80,
            height: 500                      
        }],

        xAxis: [
            {  // 几张图，几个xAxis，yAxis
            type: 'category',
            boundaryGap: false,
            data: metadata.Timestamp,
            gridIndex: 0,
        }, {  // 几张图，几个xAxis，yAxis
            type: 'category',
            boundaryGap: false,
            data: metadata.Timestamp,
            gridIndex: 1,
        }],

        yAxis: [
            {
            type: 'value',
            gridIndex: 0
        }, {
            type: 'value',
            gridIndex: 1
        }],

        series: [
            {
                name: 'Axis0Torque',
                type: 'line',
                xAxisIndex: 0,
                yAxisIndex: 0,
                data: metadata.Axis0Torque,                           
            },
            {
                name: 'Axis1Torque',
                type: 'line',
                xAxisIndex: 0,
                yAxisIndex: 0,
                data: metadata.Axis1Torque,                           
            },
            {
                name: 'Axis2Torque',
                type: 'line',
                xAxisIndex: 0,
                yAxisIndex: 0,
                data: metadata.Axis2Torque,                           
            },
            {
                name: 'Axis3Torque',
                type: 'line',
                xAxisIndex: 0,
                yAxisIndex: 0,
                data: metadata.Axis3Torque,                           
            },
            {
                name: 'Axis4Torque',
                type: 'line',
                xAxisIndex: 0,
                yAxisIndex: 0,
                data: metadata.Axis4Torque,                           
            },
            {
                name: 'Axis0Velocity',
                type: 'line',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: metadata.Axis0Velocity,                           
            },
            {
                name: 'Axis1Velocity',
                type: 'line',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: metadata.Axis1Velocity,                           
            },
            {
                name: 'Axis2Velocity',
                type: 'line',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: metadata.Axis2Velocity,                           
            },
            {
                name: 'Axis3Velocity',
                type: 'line',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: metadata.Axis3Velocity,                           
            },
            {
                name: 'Axis4Velocity',
                type: 'line',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: metadata.Axis4Velocity,                           
            }

            
        ],


    };
    return option;
}


