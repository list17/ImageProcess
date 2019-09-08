// // 配置 Mock 路径
// require.config({
//     paths: {
//         mock: 'http://mockjs.com/dist/mock'
//     }
// })
// // 加载 Mock
// require(['mock'], function(Mock){
//     // 使用 Mock
//     var data = Mock.mock({
//         'list|1-10': [{
//             'id|+1': 1
//         }]
//     })
//     // 输出结果
//     document.body.innerHTML +=
//         '<pre>' +
//         JSON.stringify(data, null, 4) +
//         '</pre>'
// })

const Mock = require('mockjs')

const courseData = function(opt) {
    return {
        data: [{
            class_name: 'gs',
            class_id: 0
        }]
    }
}

// Mock.mock('/user/get_student_classroom', /post|get/i, courseData);