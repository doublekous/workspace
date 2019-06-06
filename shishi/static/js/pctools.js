/*
    2016-02-16 dk
*/

$("#simulate").on('click', function () {
  const url = $.trim($("#url").val());
  if (check_url(url)) {
    clean_result();
    $(".clean-result").html("正在处理....");
    $.post('/pageclean/simulate_test', {
        'url': url,
        'decode_type': $("#decode_type").val(),
        'use_proxy': $("#use_proxy").is(":checked")
      },
      function (data) {
        load_result(data);
      }
    );
  }
});


$("#loadconfig").on('click', function () {
  const url = $.trim($("#url").val());
  if (check_url(url)) {
    $.post('/pageclean/load_config', {
        'url': url
      },
      function (data) {
        if (data === "err") {
          clean_config();
          load_default_config();
          alert("无当前网址配置，加载默认配置。");
          $.post('/pageclean/get_pagetype', {
              'url': url
            },
            function (data) {
              $("#get_pagetype").html(data);
              if (data !== "err") $("#pagetype").val(data);
            });
        }
        else {
          clean_config();
          load_config(data);
        }
      });

  }
});

$("#testconfig").on('click', function () {
  const url = $.trim($("#url").val());
  const configs = get_base_config();
  if (check_url(url)) {
    clean_result();
    $(".clean-result").html("正在处理....");
    $.post('/pageclean/test_config', {
        'configs': configs,
        'decode_type': $("#decode_type").val(),
        'use_proxy': $("#use_proxy").is(":checked")
      },
      function (data) {
        if (data === "err") {
          alert("配置异常,请修改配置。");
        }
        else {
          load_result(data);
        }
      });
  }
});

$("#loadjumpconfig").on('click', function () {
  const url = $.trim($("#url").val());
  if (check_url(url)) {
    $.post('/pageclean/load_jump_config', {
        'url': url
      },
      function (data) {
        if (data === "err") {
          alert("当前网址无jump配置。");
        }
        else {
          load_jump_config(data);
          alert("加载成功");
        }
      });
  }
});

$("#saveconfig").on('click', function () {
  const msg = "确定要保存配置吗？";
  if (confirm(msg) === true) {
    const config_name = $.trim($("#config_name").val());
    if (config_name === "") {
      alert("配置名称不能为空！");
      return false;
    }

    const url = $.trim($("#url").val());
    const configs = get_base_config();
    if (check_url(url)) {
      $.post('/pageclean/save_config', {
          'configs': configs
        },
        function (data) {
          if (data === "err") {
            alert("配置异常,请修改配置。");
          }
          else {
            alert("保存配置成功！");
          }
        });
    }
  } else {
    return false;
  }

});

$("#savetestset").on('click', function () {
  const msg = "确定要保存至测试集吗？";
  if (confirm(msg) === true) {
    const url = $.trim($("#url").val());
    if (check_url(url)) {
      const pagetype = $("#pagetype").val();
      const strategy = $("#strategy").val();

      const title = $.trim($(".title").html());
      const date = $.trim($(".date").html());
      const text = $.trim($(".main-text").html());

      if (title !== "" && date !== "" && text !== "") {
        $.post('/pageclean/save_testset', {
            'url': url,
            'pagetype': pagetype,
            'strategy': strategy,
            'title': title,
            'date': date,
            'text': text
          },
          function (data) {
            if (data === "err") {
              alert("系统异常,请稍后再试。");
            }
            else {
              alert("保存成功！");
            }
          });
      }
      else {
        alert("当前无完整的测试结果！");
      }
    }
  } else {
    return false;
  }
});

$("#savejumpconfig").on('click', function () {
  const msg = "确定要保存配置吗？";
  if (confirm(msg) === true) {
    const config_name = $.trim($("#jump_config_name").val());
    if (config_name === "") {
      alert("配置名称不能为空！");
      return false;
    }

    const configs = get_jump_config();
    if (check_jump_config()) {
      $.post('/pageclean/save_jump_config', {
          'configs': configs
        },
        function (data) {
          if (data === "err") {
            alert("配置异常,请修改配置。");
          }
          else {
            alert("保存配置成功！");
          }
        });
    }
  } else {
    return false;
  }
});

function check_url(url) {
  if (url === "") {
    alert("请输入url!");
    return false;
  }
  // regExp = /^((https?|ftp|news):\/\/)?([a-zA-Z]([a-zA-Z0-9\-]*[\.。])+([a-zA-Z]{2}|aero|arpa|biz|com|coop|edu|gov|info|int|jobs|mil|museum|name|nato|net|org|pro|travel)|(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))(\/[a-zA-Z0-9_\-\.~]+)*(\/([a-zA-Z0-9_\-\.]*)(\?[a-zA-Z0-9+_\-\.%=&]*)?)?(#[a-zA-Z][a-zA-Z0-9_]*)?$/
  /*var strRegex = '^((https|http|ftp|rtsp|mms)?://)'
      + '?(([0-9a-zA-Z_!~*\'().&=+$%-]+: )?[0-9a-zA-Z_!~*\'().&=+$%-]+@)?' //ftp的user@
      + '(([0-9]{1,3}.){3}[0-9]{1,3}' // IP形式的URL- 199.194.52.184
      + '|' // 允许IP和DOMAIN（域名）
      + '([0-9a-zA-Z_!~*\'()-]+.)*' // 域名- www.
      + '([0-9a-zA-Z][0-9a-zA-Z-]{0,61})?[0-9a-zA-Z].' // 二级域名
      + '[a-zA-Z]{2,6})' // first level domain- .com or .museum
      + '(:[0-9]{1,4})?' // 端口- :80
      + '((/?)|' // a slash isn't required if there is no file name
      + '(/[0-9a-zA-Z_!~*\'().;?:@&=+$,%#-]+)+/?)$';
  var regExp=new RegExp(strRegex);
  if(!(regExp.test(url))){
      alert('url格式不正确!');
      return false;
  }*/
  return true;
  //var reg=/^([hH][tT]{2}[pP]:\/\/|[hH][tT]{2}[pP][sS]:\/\/)(([A-Za-z0-9-~]+)\.)+([A-Za-z0-9-~\/])+$/;
  //if(!reg.test(url)) {
  //   return false;
  //}
  // else {
  //    return true;
  //}
}

function load_result(data) {
  if (data === undefined) {
    alert("程序异常,请重试！");
    return false;
  }
  if ("content" in data) {
    $(".clean-result").html("");
    $(".title").html(data["title"]);
    $(".date").html(data["date"]);
    $(".main-text").html(data["content"].replace('<DEL>', ''));
  }
  else {
    $(".page-type").html("网页类型：" + data["pagetype"]);
    $(".clean-result").html("未处理");
  }
}

function clean_result() {
  $(".page-type").html("");
  $(".title").html("");
  $(".date").html("");
  $(".main-text").html("");
}

function load_default_config() {
  $("#accumulate_naviblocks").val("6");
  $("#continuous_naviblocks").val("3");
  $("#delete_end_block_cnt").val("2");
  $("#full_threshold").val("0.5");
  $("#min_deleteendblock_totalBlockCnt").val("40");
  $("#min_candidate_sentCnt").val("1");
  $("#min_title_charCnt").val("8");
}

function load_config(data) {
  if (data["pagetype"] === "jump") {
    load_default_config();
    alert("无当前网址配置，加载默认配置。");
  }
  else {
    // load strategy,pagetype
    $("#strategy").val(data["strategy"]);
    $("#pagetype").val(data["pagetype"]);
    $("#get_pagetype").html(data["pagetype"]);
    // load text input
    $(".tab1 input[type='text']").each(function () {
      var key = $(this).attr("name");
      if (key in data) {
        $(this).val(data[key]);
      }
    });
    // load checkbox
    $(".tab1 input[type='checkbox']").each(function () {
      const key = $(this).attr("name");
      if (key in data) {
        if (data[key]) {
          $(this).prop("checked", true);
        }
        else {
          $(this).removeAttr("checked");
        }
      }
    });
    alert("加载成功");
  }

}

function get_base_config() {
  const configs = {};
  configs["base"] = {};
  configs["pagetype"] = $("#pagetype").val() ? $("#pagetype").val() : "news";
  configs["config_name"] = $("#config_name").val();
  configs["url"] = $.trim($("#url").val());
  configs["base"]["strategy"] = $("#strategy").val();

  $(".tab1 input[type='text']").each(function () {
    if ($.trim($(this).val()) !== "") {
      var key = $(this).attr("name");
      if (key === "config_name") {
        configs["config_name"] = $(this).val();
      }
      else {
        data = parseFloat($(this).val());
        if (!isNaN(data)) {
          configs["base"][key] = data;
        }
        else {
          configs["base"][key] = $(this).val();
        }
      }

    }
  });
  $(".tab1 input[type='checkbox']").each(function () {
    const key = $(this).attr("name");
    if (key !== "ignore_list_sentences") {
      if ($(this).is(':checked')) {
        configs["base"][key] = true;
      }
    }
    else {
      if (!$(this).is(':checked')) {
        configs["base"][key] = false;
      }
    }
  });
  return JSON.stringify(configs);
}

function load_jump_config(data) {
  $(".added").remove();
  $("#jump_config_name").val(data["config_name"]);
  let i = 1;
  for (const key in data.jumpinfo) {
    if (i === 1) {
      $(".jump_key").val(key);
      $(".jump_data").val(data.jumpinfo[key]);
    }
    else {
      const input = '<div class="m10 input-text mb10 clearfix  added"><input type="text" class="form-control whalf fl" data-flag="key" value="' + key + '" placeholder="输入内容"><input type="text" class="form-control whalf fl m10" data-flag="data" value="' + data.jumpinfo[key] + '" placeholder="输入内容"><span class="btn del-btn m10">删除</span></div>';
      $('.add-btn').parent('.form-group').prev('.undata').find('.text').append(input);
    }
    i++;
  }
}

function get_jump_config() {
  const $parent = $('.undata').find('.input-text');
  let configs = {
    base: {jumpinfo: {}},
    config_name: $("#jump_config_name").val()
  };

  $parent.each(function () {
    const _key = $($(this).children('input')[0]).val();
    const _data = $($(this).children('input')[1]).val();
    const _config = _data;
    configs["base"]["jumpinfo"][_key] = _data;
  });
  return JSON.stringify(configs);
}

function check_jump_config() {
  const $parent = $('.undata').find('.input-text').children('input');
  let flag = true;
  $parent.each(function () {
    if ($(this).val() === "") {
      flag = false;
      alert('请填写完整的配置!');
      return false;
    }
  });
  return flag;
}

function clean_config() {
  // clean strategy,pagetype
  $("#strategy").val("original");
  $("#pagetype").val("news");
  // clean text input
  $(".tab1 input[type='text']").each(function () {
    $(this).val("");
  });
  // clean checkbox
  $(".tab1 input[type='checkbox']").each(function () {
    $(this).removeAttr("checked");
  });
  $("#ignore_list_sentences").prop("checked", true);
}
