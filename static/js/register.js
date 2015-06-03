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


$('#btn_send').click(function(){
	var correo = $('#id_email').val();
	var pass_1 = $('#id_password_one').val();
	var pass_2 = $('#id_password_two').val();

	$.getJSON('/formulario/', {'correo':correo, 'pass_1':pass_1, 'pass_2':pass_2}, function(data){
		if (data == 1){
			$('#form_reset').hide();
			$('#form_success').show();
			$('#error_pass').hide();
			$('#error_user').hide();
			$('#error_pass_len').hide();
		}else if(data == 2){
			$('#error_pass').show();
			$('#error_user').hide();
			$('#form_success').hide();
			$('#error_pass_len').hide();
		}else if (data == 3){
			$('#error_user').show();
			$('#error_pass').hide();
			$('#form_success').hide();
			$('#error_pass_len').hide();
		}else{
			$('#error_pass_len').show();
			$('#error_pass').hide();
			$('#error_user').hide();
			$('#form_success').hide();
		}
	});
});

$('#btn-reset').click(function(){
	var correo = $('#input_mail').val();
	$('#loading').show();
	$.getJSON('/reset-contrasenia/', {'correo':correo}, function(data){
  		if (data == 1){
        		$('#mensaje_ok').show();
        		$('#mensaje_no').hide();
        		$('#loading').hide();
       		$('#envio_instr').hide();
    		}
    		else{
        		$('#mensaje_ok').hide();
        		$('#mensaje_no').show();
        		$('#loading').hide();
    		}
	});
});