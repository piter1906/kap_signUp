const divs = document.querySelectorAll('.basic');
for (div of divs) {
  div.addEventListener('mouseover', (e) => {
    e.target.childNodes[1].style.visibility = 'visible';
    e.target.childNodes[1].style.opacity = '1';
  });
  div.addEventListener('mouseleave', (e) => {
    e.target.childNodes[1].style.visibility = 'hidden';
    e.target.childNodes[1].style.opacity = '0';
  });
}

 function setCookie(name, value, days) {
      var expires = "";
      if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
      }
      document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }

    function getCookie(name) {
      var nameEQ = name + "=";
      var ca = document.cookie.split(';');
      for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
          c = c.substring(1, c.length);
        }
        if (c.indexOf(nameEQ) === 0) {
          return c.substring(nameEQ.length, c.length);
        }
      }
      return null;
    }

    function showCookieBanner() {
      var cookieBanner = document.getElementById("cookieBanner");
      if (!getCookie("cookiesAccepted")) {
        cookieBanner.style.display = "block";
      }
    }

    function hideCookieBanner() {
      var cookieBanner = document.getElementById("cookieBanner");
      cookieBanner.style.display = "none";
    }

    function acceptCookies() {
      setCookie("cookiesAccepted", true, 365);
      hideCookieBanner();
    }

    document.addEventListener("DOMContentLoaded", function(event) {
      showCookieBanner();

      var acceptCookiesButton = document.getElementById("acceptCookies");
      acceptCookiesButton.addEventListener("click", acceptCookies);
    });
