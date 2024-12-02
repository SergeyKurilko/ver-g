$(document).ready(function () {
    $('#EducationPlatformNavbarMenuButton').click(function (e) { 
        if ($('#EducationPlatformNavbarMenuButton').hasClass('collapsed')) {
            $('.auth-button-group-wrapper').removeClass('align-self-start').removeClass('mt-7-px');
            $('.auth-button-group-wrapper').addClass('align-self-center');
        } else {
            $('.auth-button-group-wrapper').removeClass('align-self-center');
            $('.auth-button-group-wrapper').addClass('align-self-start').addClass('mt-7-px');
        } ;
    });
   
});