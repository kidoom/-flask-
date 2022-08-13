function bindCaptchaBtnClick(){
    $("#captcha-btn").on("click",function (event){
        var $this = $(this)
       var email = $("input[name='email']").val();
       if(!email){
           alert("请先输入邮箱！");
           return;
       }
       // 通过js发送网络请求： ajax
       $.ajax({
           url:"/captcha",
           method:"POST",
           data:{
               "email":email
           },
           success:function (res){
                var code = res['code']
                if (code == 200){
                    //取消点击事件
                    $this.off("click")
                    // 开始倒计时
                    var countdown = 60;
                 var timer =   setInterval(function (){
                     countdown -= 1;
                     if (countdown>0){
                            $this.text(countdown+"秒后重新发送");
                        }else{
                            $this.text("获取验证码")
                            //重回执行函数 ，重新绑定点击事件
                            bindCaptchaBtnClick();
                            // 如果不需要倒计时，那么就要清除倒计时， 否则会一直进行下去
                            clearInterval(timer);
                        }
                    },1000)

                    alert("验证码发送成功")
                }else{
                    alert(res['message'])
                }
           }
       })
    });
}
// 等待文档所有元素加载完成后执行
$(function (){
    bindCaptchaBtnClick();
});