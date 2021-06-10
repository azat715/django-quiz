// Avoid `console` errors in browsers that lack a console.
(function () {
  var method;
  var noop = function () { };
  var methods = [
    'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
    'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
    'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
    'timeline', 'timelineEnd', 'timeStamp', 'trace', 'warn'
  ];
  var length = methods.length;
  var console = (window.console = window.console || {});

  while (length--) {
    method = methods[length];

    // Only stub undefined methods.
    if (!console[method]) {
      console[method] = noop;
    }
  }
}());


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function quizzes() {
  return {
    csrftoken: getCookie('csrftoken'),
    tab: "all",
    quizzes: [],
    fetchQuizzes(url) {
      fetch(url)
        .then(response => response.json())
        .then(data => {
          this.quizzes = data;
        });
    },
    startQuiz: function (quizz) {
      fetch("/api/quizzes/started", {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFToken': this.csrftoken
        },
        body: JSON.stringify({ "uuid": quizz.uuid })
      }).then(response => response.json())
        .then(() => {
          location.href = `quizz/${quizz.slug}`
        })
        .catch((error) => {
          console.log('Request failed', error);
        });
    },
  }
}

function question(base) {
  return {
    baseURL: base,
    questionURL: base + '/question',
    scoreURL: base + '/score',
    questionPrevURL: base + '/question' + '/prev',
    csrftoken: getCookie('csrftoken'),
    answer: null,
    choices: [],
    text: "",
    question_uuid: "",
    res: "",
    show: false,
    prev: false,
    button_prev: true,
    fetchQuestion() {
      fetch(this.questionURL)
        .then(response => response.json())
        .then(data => {
          if (data.status == "the questions are over") {
            return Promise.reject();
          }
          else {
            return data
          }
        })
        .then(data => {
          this.choices = data.choices;
          this.text = data.text
          this.question_uuid = data.uuid
        })
        .catch(() => {
          this.get_score()
        });
    },
    send() {
      form = document.getElementById("form");
      formData = new FormData(form);
      let data = {
        "question_uuid": this.question_uuid,
        "choices": formData.getAll("choice")
      }
      if (!this.prev) {
        fetch(this.questionURL, {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': this.csrftoken
          },
          body: JSON.stringify(data)
        }).then(response => response.json())
          .then(() => {
            this.fetchQuestion(this.questionURL);
          })
          .catch((error) => {
            console.log('Request failed', error);
          });
      } else {
        fetch(this.questionURL, {
          method: 'PATCH',
          credentials: 'include',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': this.csrftoken
          },
          body: JSON.stringify(data)
        }).then(() => {
          this.fetchQuestion(this.questionURL);
        })
          .catch((error) => {
            console.log('Request failed', error);
          });
        this.prev = false
        this.questionURL = this.baseURL + '/question'
      }
      this.button_prev = false
    },
    get_score() {
      fetch(this.scoreURL)
        .then(response => response.json())
        .then(data => {
          this.res = data.score;
          this.show = true;
        });
    },
    get_prev(event) {
      event.disable
      this.questionURL = this.questionPrevURL
      this.prev = true
      this.button_prev = true
      this.fetchQuestion()
    }

  }
}