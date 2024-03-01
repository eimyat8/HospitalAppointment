function setClock() {
        const days = [
          "Sunday",
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday",
        ];
        const getdate = new Date();
        let gethours = getdate.getHours();
        let getmins = getdate.getMinutes();
        let getsec = getdate.getSeconds();
        let getday = getdate.getDay();
        let getampm;

        switch (gethours > 12) {
          case true:
            getampm = "PM";
            gethours = gethours - 12;
            break;
          case false:
            getampm = "AM";
            break;
        }
        let setclock = `${gethours} : ${getmins} : ${getsec} ${getampm} ${days[getday]}`;
        document.getElementById("time").innerHTML = setclock;
      }
      setClock();
      setInterval(setClock, 1000);