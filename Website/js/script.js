$(document).ready(function() {
  // Adding a "Javascripts is Enabled" Body Class
  // Below is for progressive enhancement
  $("body").addClass("js");

  // A popup will appear whenever user clicks reservation
  $("#page-header .booking a, #reservation_date_occupancy .close-button a").click(function(event) {
    event.preventDefault();
    $("body").toggleClass("reservation_commence")
  });

  // After user clicks popup, will submit information about arrival and departure dates - this will check that all values filled and stores information into local storage and will be used in next page
  $("#page-header #reservation_date_occupancy .submit_button_reservation_start a").click(function(event) {
    event.preventDefault();
    
    var arrival_date = $("#arrival_date_value").val();
    var departure_date = $("#departure_date_value").val();
    var kids_num = $("#kids_number option:selected").val();
    var adults_num = $("#adult_number option:selected").val();
    console.log(kids_num);
    var total_check = parseInt(kids_num) + parseInt(adults_num);

    // if any of the fields are empty, and error will be produced which will let the user know
    if (arrival_date == "" || departure_date == "" || total_check == 0) {

      if (total_check == 0) {
        $('#reservation_date_occupancy .adult_guest select').addClass("error_found");
        $('#reservation_date_occupancy .kids_guest select').addClass("error_found");
        $('#reservation_date_occupancy .occupancy p').addClass("error_found");
      } else {
        $('#reservation_date_occupancy .adult_guest select').removeClass("error_found");
        $('#reservation_date_occupancy .kids_guest select').removeClass("error_found");
        $('#reservation_date_occupancy .occupancy p').removeClass("error_found");
      } 


      if (arrival_date == "" || departure_date == "") {
        $('#reservation_date_occupancy .arrival p').addClass("error_found");
        $('#reservation_date_occupancy .departure p').addClass("error_found");
        $('#reservation_date_occupancy .arrival input').addClass("error_found");
        $('#reservation_date_occupancy .departure input').addClass("error_found");
      } else {
        $('#reservation_date_occupancy .arrival p').removeClass("error_found");
        $('#reservation_date_occupancy .departure p').removeClass("error_found");
        $('#reservation_date_occupancy .arrival input').removeClass("error_found");
        $('#reservation_date_occupancy .departure input').removeClass("error_found");
      }

    } else {
      // store values 
      localStorage.setItem('arrival', arrival_date);
      localStorage.setItem('departure', departure_date);
      localStorage.setItem('kids_num', kids_num);
      localStorage.setItem('adult_num', adults_num);

      // Takes user to reservation page for review
      location.href = 'reservation_step_1.html';

      // Set value for user's confirmation
      arrival_date = localStorage.getItem('arrival');
      departure_date = localStorage.getItem('departure');

      $("#reservation_dates_guests_step_1 #departure_date_value input:date").val(arrival_date);
    }
  });

  // checks for number of occupancy arriving to display the right number of forms for the number of guest details to be filled
  if (localStorage.getItem('kids_num') > 0 || localStorage.getItem('adult_num') > 0) {
    
    var kids_num = localStorage.getItem('kids_num');
    var adult_num = localStorage.getItem('adult_num');
    var total_forms_needed = parseInt(adult_num) + parseInt(kids_num);

    // based on number of guests coming, number of forms will be displayed accordingly
    if (total_forms_needed > 1) {
      $(".guest_2_form").addClass('required');
    } 
    
    if (total_forms_needed > 2) {
      $(".guest_3_form").addClass('required');
    } 
    
    if (total_forms_needed > 3) {
      $(".guest_4_form").addClass('required');
    }
  }

  // checks to ensure all forms are filled correctly and lets user know if anything is missing
  $("#reservation_step_2 .submit_button_reservation_step_2 .verify").click(function(event) {
    event.preventDefault();
    // tracks if all forms have been filled - inclusive of room
    var count = 0;

    // checks if any rooms have been selected
    var room1 = $("#room1_qty option:selected").val();
    var room2 = $("#room2_qty option:selected").val();
    var room3 = $("#room3_qty option:selected").val();
    var room4 = $("#room4_qty option:selected").val();
    var num_rooms_selected = parseInt(room1) + parseInt(room2) + parseInt(room3) + parseInt(room4);

    if (num_rooms_selected == 0) {
      $("#reservation_rooms_guests_step_2 .manage_room p").addClass('error_found');
      $("#reservation_rooms_guests_step_2 .manage_room select").addClass('error_found');

    } else {
      count = count + 1;
      if ($("#reservation_rooms_guests_step_2 .manage_room p").hasClass('error_found')) {
        $("#reservation_rooms_guests_step_2 .manage_room p").removeClass('error_found');
        $("#reservation_rooms_guests_step_2 .manage_room select").removeClass('error_found');
      }
    }

    var forms_available = [".guest_1_form",".guest_2_form", ".guest_3_form", ".guest_4_form"];
    var forms_to_check = [];

    // check forms that exist on webpage - do not need to check all
    for (var i = 0; i < total_forms_needed; i++) {
      forms_to_check.push(forms_available[i]);
    }

    var formsLength = forms_to_check.length;
    var fName = " input#first_name"
    var lName = " input#last_name"
    var email = " input#email_address"
    var country = " input#origin_country_from"
    var phone = " input#guest_contact_num"

    // go through all forms and check if anything is left blank
    for (var i = 0; i < formsLength; i++) {
      
      var fName_check = forms_to_check[i].concat(fName);
      var lName_check = forms_to_check[i].concat(lName);
      var email_check = forms_to_check[i].concat(email);
      var country_check = forms_to_check[i].concat(country);
      var phone_check = forms_to_check[i].concat(phone);
      var error = "#reservation_rooms_guests_step_2 ".concat(forms_to_check[i]);

      // checks each input to ensure that they are filled
      if ($(fName_check).val() == "" || $(lName_check).val() == "" || $(email_check).val() == "" || $(country_check).val() == "" || $(phone_check).val() == "") {
        $(error).addClass('error_found')

      // since all inputs are filled and error_found class can still be found, we remove it so guests would not be confused
      } else if ($(error).hasClass('error_found')) {
        $(error).removeClass('error_found')
      }

      // number of forms filled correctly - count will be updated and if user leaves form empty again (after inserting a value into input), count will be updated
      if ($(fName_check).val() != "" || $(lName_check).val() != "" || $(email_check).val() != "" || $(country_check).val() != "" || $(phone_check).val() != "") {
        count = count + 1
      } else if (count > 1) {
        count = count - 1
      }

      // once count meets criteria - user will be taken to last step of reservation
      if (count == 1 + formsLength) {
        location.href = 'reservation_step_3.html';
      }
    }
  });

  // if statement will run whenever a page is run, but only input value in reservation_step_1.html will be updated
  if (localStorage.getItem('arrival') !== null) {
    var guest_arrive = localStorage.getItem('arrival');
    var guest_depart = localStorage.getItem('departure');
    var kids_num = localStorage.getItem('kids_num');
    var adult_num = localStorage.getItem('adult_num');
    var duration_of_stay = 0;

    // set values in reservation_step_1.html
    $("#reservation_dates_guests_step_1 input#arrival_date_value").val(guest_arrive);
    $("#reservation_dates_guests_step_1 input#departure_date_value").val(guest_depart);
    $("#reservation_dates_guests_step_1 select#adult_number").val(adult_num);
    $("#reservation_dates_guests_step_1 select#kids_number").val(kids_num);

    // this will be updated with number of days guest will be staying and number of guest visiting the resort
    var length_of_stay = "Length of Stay : ";
    var number_of_guest = "Occupancy Expected : ";

    var date_format_depart = new Date(guest_depart);
    var date_format_arrival = new Date(guest_arrive);
    var diff_in_time = date_format_depart.getTime() - date_format_arrival.getTime();
    var diff_in_day = diff_in_time / (1000 * 3600 * 24);

    length_of_stay = length_of_stay + diff_in_day.toString();
    var total_guest = parseInt(adult_num) + parseInt(kids_num);
    number_of_guest = number_of_guest + total_guest.toString();

    $("#date_guest_num_confirmation #days_num .length_of_stay").html(length_of_stay);
    $("#date_guest_num_confirmation #guest_num .num_guest_stay").html(number_of_guest);
  }

  // dropdown menu 
  $("#main-menu-dropdown .drop_button").click(function(event) {
    event.preventDefault();

    $('#hamburger_dropdown').toggleClass("show");

    // looks for any <li></li> tag in html and if there is - goes into this block of code
    $('#hamburger_dropdown li').each(function () {

      // once user presses and repress the same button, we remove the show class to reverse the effect of the 'dropdown'
      if ($(this).find('a').hasClass('show')) {
        $(this).find('a').removeClass('show');
      }
    });
  });

  // expand collapse functionality for rooms
  $("#rooms_activities .services .more_information").click(function(event) {
    event.preventDefault();

    var temp = '#'.concat(this.id);
    var additional_info = temp.concat(' em');
    var check_content = '';

    // so that only specific section will be displayed when a specific section is clicked. This allows for only one section to be displayed or hidden if clicked again for each room and activities
    if (this.id == 'activity1_info') {
      check_content = '.js .content_activity1';
    } else if (this.id == 'activity2_info') {
      check_content = '.js .content_activity2';
    } else if (this.id == 'activity3_info') {
      check_content = '.js .content_activity3';
    } else if (this.id == 'activity4_info') {
      check_content = '.js .content_activity4';

    } else if (this.id == 'room1_info') {
      check_content = '.js .content_room1';
    } else if (this.id == 'room2_info') {
      check_content = '.js .content_room2';
    } else if (this.id == 'room3_info') {
      check_content = '.js .content_room3';
    } else if (this.id == 'room4_info') {
      check_content = '.js .content_room4';
    }

    // user will know if content has been collapsed or not when icon changes
    if ($(check_content).css('display') == 'none') {

      $(check_content).css('display', 'block');
      $(additional_info).removeClass("fa fa-plus").addClass("fas fa-minus");

    } else {
      $(check_content).css('display', 'none');
      $(additional_info).removeClass("fa fa-minus").addClass("fas fa-plus");
    }
  });

  // 2 buttons clicked will check if is already highlighted on website or not - if it is it will do nothing but if is it will highlight the directions needed to be shown 
  $(".ship_directions").click(function(event) {
    event.preventDefault();

    if ($(this).hasClass("highlight_clicked")) {
    } else {
      $(this).addClass("highlight_clicked");
      $("#for_ship").addClass("highlight_clicked");

      $("#plane_dir").removeClass("highlight_clicked");
      $("#for_plane").removeClass("highlight_clicked");
    }
  });

  $(".plane_directions").click(function(event) {
    event.preventDefault();

    if ($(this).hasClass("highlight_clicked")) {
    } else {
      $(this).addClass("highlight_clicked");
      $("#for_plane").addClass("highlight_clicked");

      $("#ship_dir").removeClass("highlight_clicked");
      $("#for_ship").removeClass("highlight_clicked");
    }
  });

  $(window).scroll(function() {
    // measures distance from the top of the document which escapes user's sight when scrolling
    var scroll = $(window).scrollTop();

    // gives height of the whole document
    var dh = $(document).height();

    // measures height of window size
    var wh = $(window).height();

    // gives value that will determine the width that will be used to fill the horizontal indicator
    var value = (scroll / (dh-wh)) * 100;

    // indicator will be shown when user scrolls pass the reservation position on webpage
    var indicator_start = $(".booking").offset().top;
    var start_indicator_value  = (indicator_start / (dh-wh)) * 100;

    var value = (scroll / (dh-wh)) * 100;

    // changes the width indicator so user knows where they are currently at on webpage 
    var adjust_width = value - start_indicator_value;
    $('#horizontal_indicator').css('width', adjust_width + '%')

    if (value > start_indicator_value) {
      if ($('#horizontal_indicator').css('display') == 'none') {

        $('#horizontal_indicator').css('display', 'block');
  
      }
    } else {
      // if indicator is already displayed - we want to then hide it once again
      if ($('#horizontal_indicator').css('display') == 'block') {
        $('#horizontal_indicator').css('display', 'none');
      } 
    }
  })

  // for dates to slide from left to right in about_us webpage
  $('.image-slide').scrollClass();
});
