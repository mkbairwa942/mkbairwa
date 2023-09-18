const container = document.querySelector(".container"),
      pwShowHide = document.querySelectorAll(".showHidePw"),
      pwFields = document.querySelectorAll(".password");
    //   signUp = document.querySelectorAll(".signup-link"),
    //   login = document.querySelectorAll(".login-link");

    //  js code to show/hide passwordnand change icon

    pwShowHide.forEach(eyeIcon =>{
        eyeIcon.addEventListener("click", ()=>{
            pwFields.forEach(pwFields =>{
                if(pwFields.type ==="password"){
                    pwFields.type = "text";

                    pwShowHide.forEach(icon =>{
                        icon.classList.replace("uil-eye-slash", "uil-eye");
                    })
                }else{
                    pwFields.type = "password";

                    pwShowHide.forEach(icon =>{
                        icon.classList.replace("uil-eye", "uil-eye-slash");
                    })
                }
            })
        }) 
    })

    // js code to appear signup and login form
    // signUp.addEventListener("click", ( )=>{
    //     container.classList.add("active");
    // });
    // login.addEventListener("click", ( )=>{
    //     container.classList.remove("active");
    // });
