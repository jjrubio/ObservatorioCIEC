$(function() {
    $( "#user_form" ).validate({

        rules: {
            first_name: {
                required: true
            },
            last_name: {
                required: true
            },
            email: {
                required: true,
                email: true
            },
            password_one: {
                required: true,
                minlength: 5
            },
            password_two: {
                required: true,
                minlength: 5,
                equalTo: "#id_password_one"
            },
            institution: {
                required: true
            },
            telefono: {
                required: true,
                digits: true
            },
            direccion: {
                required: true
            },
            grado_academico: {
                required: true
            },

        },
        messages: {
            first_name: {
                required: "Por favor ingrese su primer nombre"
            },
            last_name: {
                required: "Por favor ingrese su primer apellido"
            },
            email: {
                required: "Por favor ingrese su correo electrónico",
                email: "Por favor ingrese un correo electrónico valido"
            },
            password_one: {
                required: "Por favor ingrese una contraseña",
                minlength: "Su contraseña debe contener al menos 5 caracteres"
            },
            password_two: {
                required: "Por favor ingrese la contraseña anterior",
                minlength: "Su contraseña debe contener al menos 5 caracteres",
                equalTo: "Por favor repita la contraseña anterior"
            },
            institution: {
                required: "Por favor ingrese la institución"
            },
            telefono: {
                required: "Por favor ingrese su número de contacto",
                digits: "Por favor ingrese solo números"
            },
            direccion: {
                required: "Por favor ingrese su dirección domiciliaria"
            },
            grado_academico: {
                required: "Por favor escoja un grado acádemico"
            },
        },
    });

});