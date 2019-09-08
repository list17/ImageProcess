export default {
  install(Vue, options) {
    Vue.prototype.formatDate = function (timestamp) {
      let date = new Date(timestamp);
      let Y = date.getFullYear() + '-';
      let M = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) + '-' : date.getMonth() + 1 + '-';
      let D = date.getDate() < 10 ? '0' + date.getDate() + ' ' : date.getDate() + ' ';
      let h = date.getHours() < 10 ? '0' + date.getHours() + ':' : date.getHours() + ':';
      let m = date.getMinutes() < 10 ? '0' + date.getMinutes() + ':' : date.getMinutes() + ':';
      let s = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds();
      return Y + M + D + h + m + s
    };
    Vue.prototype.Const = {
      ProblemLanguage: {
        JavaScript: 0,
        HTML: 1,
        Python2: 2,
        C: 3,
        Cpp: 4,
        Python3: 5,
        Java: 6,
      },
      MatchType: {
        Friendly: 0,
        Ranking: 1
      },
      MatchResult: {
        Win: 0,
        Lose: 1,
        TBD: 2
      },
      ProblemOwnership: {
        InProblemSet: 0,
        InClassroom: 1
      },
      DDLType: {
        DDL_FOREVER: 0,
        DDL_STRICT: 1,
        DDL_PENALTY: 2,
      },
      ProblemStatus: {
        Unpublished: 0,
        Published: 1,
        Deleted: 2,
      },
      ProblemTestType: {
        strict: 0,
        ignore_space: 1,
        ignore_order: 2
      },
      SubmissionErrorType: {
        NO_ERROR: 0,
        ERROR_FUNCTION_NOT_FOUND: 1,
        ERROR_TIME_OUT: 2,
        ERROR_MEMORY_OUT: 3,
        ERROR_RUNTIME: 4,
        ERROR_COMPILE: 5,
        ERROR_UNKNOWN: 233,
      },
      SubmissionCreator: {
        USER: 1,
        SYSTEM: 2
      }


    }
  }
}
