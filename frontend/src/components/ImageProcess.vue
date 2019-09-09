<template>
<div>
  <div class="demo-image">
    <div class="block" v-for="text in texts" :key="text['fit']">
      <span class="demonstration">{{ text["text"] }}</span>
      <el-image
        style="width: 100%; height: 100%"
        :src="text['url']"
        :fit="text['fit']">
      </el-image>
    </div>
  </div>
  <div class="button-group">
    <div class="button-display">
      <el-form :model="form">
          <el-upload
            ref="upload"
            action="api/filetransfer/upload/"
            accept="image/png,image/gif,image/jpg,image/jpeg"
            list-type="picture-card"
            :limit=1
            :auto-upload="false"
            :on-exceed="handleExceed"
            :before-upload="handleBeforeUpload"
            :on-preview="handlePictureCardPreview"
            :on-remove="handleRemove"
            :on-success="uploadSuccess"
            :on-change="changeFile">
            <i class="el-icon-plus"></i>
          </el-upload>
          <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="">
          </el-dialog>
        <el-form-item style="display:flex; justify-content:space-around ;">
          <el-button size="small" type="primary" @click="uploadFile">立即上传</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class='button-display2'>
      <el-button @click='FindFaces' size='big'>找到人脸</el-button>
      <el-button @click='demo2' size='big'>demo2</el-button>
      <el-button @click='download' size='big'>下载图片</el-button>
    </div>
  </div>
</div>
</template>

<script>
  export default {
    name:'image_processing',
    components:{

    },
    props: {
      max: {
        type: Number,
        default: 1
      },
      value: Array
    },
    data() {
      return {
        dialogImageUrl: '',
        dialogImageChangedUrl: '',
        // dialogImageChangedUrlList: [],
        fileUpload:{"is_url": false, "url": '' },
        texts:[
          {"text":'处理前',"fit":'contain','url':""},
          {"text":'处理后',"fit":'fill','url':""}
        ],
        dialogVisible: false,
        formLabelWidth: '80px',
        limitNum: 3,
        form: {}
      }
    },
    mounted() {

    },
    methods: {
      FindFaces(){
        let params = new URLSearchParams()
        // params.append('url', dialogImageUrl)
        this.$axios.post('/features/faceemoji',params).then(response => {
          this.texts[1]['url']  = response.data['url'];
        })
      },
      demo2(){

      },
      download(){
        this.$confirm('开始下载图片','确认').then(()=>{

        })
      },
      handleBeforeUpload(file){
        if(!(file.type === 'image/png' || file.type === 'image/gif' || file.type === 'image/jpg' || file.type === 'image/jpeg')) {
          this.$notify.warning({
            title: '警告',
            message: '请上传格式为image/png, image/gif, image/jpg, image/jpeg的图片'
          })
        }
        let size = file.size / 1024 / 1024 / 2
        if(size > 2) {
          this.$notify.warning({
            title: '警告',
            message: '图片大小必须小于2M'
          })
        }
      },

      handleExceed(files, fileList) {
        this.$confirm('文件个数超出限制，请点击图片中的删除按钮删除后进行再次上传','确认');
      },
      handleRemove(file, fileList) {
        this.dialogImageUrl = "";
        this.texts[0]['url'] = "";
        this.texts[1]['url'] = "";
      },
      handlePictureCardPreview(file) {
        this.dialogImageUrl = file.url;
        this.texts[0]['url'] = file.url;
        this.dialogVisible = true;
      },
      changeFile(file, fileList){
        if(typeof file.url === "string"){
          this.dialogImageUrl = file.url;
          this.texts[0]['url'] = file.url;
        }
      },
      uploadFile() {
        this.$refs.upload.submit();
      },
      uploadSuccess(response, file, fileList) {
        this.$confirm(response['msg'],"确认");
      }
    }
  }

</script>

<style scoped>
.block {
  width:40%;
  height:80%;
}
.demo-image{
  width:100%;
  display:flex;
  flex-direction:row;
  justify-content:space-around ;
}
.demonstration{
  display:flex;
  justify-content:center;
  padding-bottom:20px;
}

/* 按钮排布 */
.button-display{
  padding-top: 40px;
  display:flex;
  justify-content:center;
  width:50%;
  padding-bottom:50px;
	margin:0 auto;
}
.button-display2{
  padding-top: 0;
  display:flex;
  justify-content:center;
  width:50%;
  padding-bottom:50px;
	margin:0 auto;
}
.button-group {
  display:flex;
  justify-content:center;
  flex-direction:column;
  width:100%;
  padding-bottom:50px;
}
</style>
