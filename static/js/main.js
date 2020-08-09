$(document).ready(function(){

  $("#add_button").click(function(){
    $("#keypair").append(`
      <div id="keypairtemp">
        <br>
        <div class="row">
          <div class="col">
            <input type="text" name="key" class="form-control" placeholder="Key">
          </div>
          <div class="col">
            <input type="text" name="value" class="form-control" placeholder="Value">
          </div>
          <div class="col-1">
            <span class="material-icons vertical-center" onClick="$(this).closest('#keypairtemp').remove();">
              clear
            </span>
          </div>
        </div>
      </div>`);
  });

  $("#fetch_button").click(function(){
    let id = $("#show_id").val();
    if(id == "")
    {
      AJAXPromise("GET", "/api/v1/show/members").then((success_data) => {
          $('#output').html(JSON.stringify(success_data,null, 1));
      },(error)=>{
        $('#output').html(JSON.stringify(error["responseJSON"],null, 1));
      });
    }
    else
    {
      AJAXPromise("GET", "/api/v1/show/members/"+id).then((success_data) => {
          $('#output').html(JSON.stringify(success_data,null, 1));
      },(error)=>{
        $('#output').html(JSON.stringify(error["responseJSON"],null, 1));
      });
    }
  });

  $("#add_member_button").click(function(){
    let id = $("#add_member_id").val();
    if(id == "")
    {
      alert("ID is missing");
      return;
    }

    let data = {
      'id' : id,
      'real_name' : $("#add_member_name").val(),
      'tz' : $("#timezone").val()
    }

    AJAXPromise("POST", "/api/v1/add/member",data).then((success_data) => {
        alert(JSON.stringify(success_data,null, 1));
    },(error)=>{
      alert(JSON.stringify(error["responseJSON"],null, 1));
    });

  });

  $("#add_activity_period_button").click(function(){
    let id = $("#id_add_activity").val();
    if(id == "")
    {
      alert("ID is missing");
      return;
    }
    let monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    start_time = new Date($("#start_time").val());
    end_time = new Date($("#end_time").val());


    let data = {
      'id' : id,
      'start_time' : monthNames[start_time.getMonth()]+" "+start_time.getDate()+" "+start_time.getFullYear()+" "+to12Hrs(start_time),
      'end_time' : monthNames[end_time.getMonth()]+" "+end_time.getDate()+" "+end_time.getFullYear()+" "+to12Hrs(end_time)
    }

    AJAXPromise("POST", "/api/v1/add/activity_period/"+id,data).then((success_data) => {
        alert(JSON.stringify(success_data,null, 1));
    },(error)=>{
      alert(JSON.stringify(error["responseJSON"],null, 1));
    });

  });

  $("#update_member_button").click(function(){
    let id = $("#id_update_member").val();
    if(id == "")
    {
      alert("ID is missing");
      return;
    }
    let data = {};
    for(let element = 0 ;  element < $('input[name="key"]').length; element++ )
    {
      let key = document.getElementsByName("key")[element].value;
      let value = document.getElementsByName("value")[element].value;
      if(key == "" || value == "")
      {
        continue;
      }
      data[key] = value;

    }

    AJAXPromise("PUT", "/api/v1/update/member/"+id,data).then((success_data) => {
        alert(JSON.stringify(success_data,null, 1));
    },(error)=>{
      alert(JSON.stringify(error["responseJSON"],null, 1));
    });
  });

  $("#delete_member_button").click(function(){
    let id = $("#id_delete").val();
    if(id == "")
    {
      alert("ID is missing");
      return;
    }

    if (confirm("Press Ok to Delete ID : "+id)) {
      AJAXPromise("DELETE", "/api/v1/delete/member/"+id).then((success_data) => {
          alert(JSON.stringify(success_data,null, 1));
      },(error)=>{
        alert(JSON.stringify(error["responseJSON"],null, 1));
      });
  }
  
  });

  $("#add_member_tab").click(function(){

    $("#add_member_tab").addClass('active');
    $("#show_members_tab").removeClass('active');
    $("#add_activity_period_tab").removeClass('active');
    $("#update_member_tab").removeClass('active');
    $("#delete_member_tab").removeClass('active');

    $("#add_member").removeClass('hide');
    $("#show_members").addClass('hide');
    $("#add_activity_period").addClass('hide');
    $("#update_member").addClass('hide');
    $("#delete_member").addClass('hide');

  });

  $("#show_members_tab").click(function(){

    $("#add_member_tab").removeClass('active');
    $("#show_members_tab").addClass('active');
    $("#add_activity_period_tab").removeClass('active');
    $("#update_member_tab").removeClass('active');
    $("#delete_member_tab").removeClass('active');

    $("#add_member").addClass('hide');
    $("#show_members").removeClass('hide');
    $("#add_activity_period").addClass('hide');
    $("#update_member").addClass('hide');
    $("#delete_member").addClass('hide');

  });

  $("#add_activity_period_tab").click(function(){

    $("#add_member_tab").removeClass('active');
    $("#show_members_tab").removeClass('active');
    $("#add_activity_period_tab").addClass('active');
    $("#update_member_tab").removeClass('active');
    $("#delete_member_tab").removeClass('active');

    $("#add_member").addClass('hide');
    $("#show_members").addClass('hide');
    $("#add_activity_period").removeClass('hide');
    $("#update_member").addClass('hide');
    $("#delete_member").addClass('hide');

  });

  $("#update_member_tab").click(function(){

    $("#add_member_tab").removeClass('active');
    $("#show_members_tab").removeClass('active');
    $("#add_activity_period_tab").removeClass('active');
    $("#update_member_tab").addClass('active');
    $("#delete_member_tab").removeClass('active');

    $("#add_member").addClass('hide');
    $("#show_members").addClass('hide');
    $("#add_activity_period").addClass('hide');
    $("#update_member").removeClass('hide');
    $("#delete_member").addClass('hide');

  });

  $("#delete_member_tab").click(function(){

    $("#add_member_tab").removeClass('active');
    $("#show_members_tab").removeClass('active');
    $("#add_activity_period_tab").removeClass('active');
    $("#update_member_tab").removeClass('active');
    $("#delete_member_tab").addClass('active');

    $("#add_member").addClass('hide');
    $("#show_members").addClass('hide');
    $("#add_activity_period").addClass('hide');
    $("#update_member").addClass('hide');
    $("#delete_member").removeClass('hide');

  });
});

function AJAXPromise(method, URL) {
    let data = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : null;
    let processData = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
    let contentType = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : 'application/x-www-form-urlencoded; charset=UTF-8';

    return new Promise(function (resolve,completed) {
        $.ajax({
            type: method,
            url: URL,
            data: data,
            processData: processData,
            contentType: contentType,
            success: function success(data)
            {
                resolve(data);
            },
            complete: function complete(data)
            {
                completed(data);
            }
        });
    });
}

function to12Hrs(time)
{
  let H = time.getHours();
  let h = H % 12 || 12;
  let ampm = (H < 12 || H === 24) ? "AM" : "PM";
  return h +":"+ time.getMinutes() + ampm;
}
