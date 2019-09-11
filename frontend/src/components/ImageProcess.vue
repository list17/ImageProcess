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

<div style="margin: 20px;"></div>

  <div style="margin-top:50px;">
    <div style="width:50%;margin:0 auto;">
      <el-form label-width="100px">
        <el-form-item label="通过url上传:">
          <el-input
          :disabled="inputDisabled"
          placeholder="请输入图片链接，可以通过在浏览器图片点击右键选择复制链接得到，支持后缀名为.jpg/.jpeg/.png"
          v-model="texts[0]['url']"
          clearable></el-input>
        </el-form-item>
        <el-form-item label="本地图片上传:">
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
                  <img width="100%" :src="texts[0]['url']" alt="">
                </el-dialog>
              <el-form-item style="display:flex; justify-content:space-around ;">
                <el-button size="small" type="primary" @click="uploadFile">立即上传</el-button>
              </el-form-item>
            </el-form>
          </div>

        </el-form-item>
      </el-form>
    </div>
    <div class="button-group">

      <div class='button-display2'>
        <el-button v-loading.fullscreen.lock="isloading" @click='FindFaces' size='big'>一键"美颜"</el-button>
        <el-button v-loading.fullscreen.lock="isloading" @click='Segmentation' size='big'>图片分割</el-button>
        <el-button @click='download' size='big'>下载图片</el-button>
      </div>
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
        fileUpload:{"is_url": false, "url": '' },
        texts:[
          {"text":'处理前',"fit":'contain','url':""},
          {"text":'处理后',"fit":'fill','url':""}
        ],
        dialogVisible: false,
        form: {},
        isloading: false,
        inputDisabled: false
      }
    },
    methods: {
      FindFaces(){
        this.isloading = true
        this.$axios.post('/features/faceemoji').then(response => {
          this.texts[1]['url']  = response.data['url'];
          this.isloading = false;
        })
      },
      Segmentation(){
        this.isloading = true
        this.$axios.post('/features/segmentation').then(response => {
          this.texts[1]['url']  = response.data['url'];
          this.isloading = false;
        }).catch((err) => {
          this.isloading = false;
          this.$confirm("处理失败");
        })
      },
      download(){
        this.$confirm('开始下载图片','确认').then(()=>{
          let url = '/api/filetransfer/download_file/?path=' + this.texts[1]['url'];
          window.open(url,'_blank');
        })
      },

      handleBeforeUpload(file){
        if(!(file.type === 'image/png' || file.type === 'image/jpg' || file.type === 'image/jpeg')) {
          this.$notify.warning({
            title: '警告',
            message: '请上传格式为image/png, image/jpg, image/jpeg的图片'
          })
        }
        let size = file.size / 1024 / 1024
        if(size > 1) {
          this.$notify.warning({
          title: '警告',
            message: '图片大小必须小于500kb'
          })
        }
      },

      handleExceed(files, fileList) {
        this.$confirm('文件个数超出限制，请点击图片中的删除按钮删除后进行再次上传','确认');
      },
      handleRemove(file, fileList) {
        this.texts[0]['url'] = "";
        this.texts[1]['url'] = "";
        this.inputDisabled = false
      },
      handlePictureCardPreview(file) {
        this.texts[0]['url'] = file.url;
        this.inputDisabled = true
        this.dialogVisible = true;
      },
      changeFile(file, fileList){
        if(typeof file.url === "string"){
          this.texts[0]['url'] = file.url;
          this.inputDisabled = true
        }
      },
      uploadFile() {
        if(this.inputDisabled){
          this.$refs.upload.submit();
        }else{
          if(this.texts[0]['url'].split('.')[this.texts[0]['url'].split('.').length - 1] !== 'jpeg' &&
          this.texts[0]['url'].split('.')[this.texts[0]['url'].split('.').length - 1] !== 'jpg' &&
          this.texts[0]['url'].split('.')[this.texts[0]['url'].split('.').length - 1] !== 'png'){
            this.$confirm("链接不正确，请重新输入")
            this.texts[0]['url'] = ""
            return
          }
          let params = new URLSearchParams()
          params.append('is_url',true)
          params.append('url',this.texts[0].url)
          this.$axios.post('api/filetransfer/upload/', params).then((response)=>{
            this.$confirm(response.data['msg'],"确认");
          })
        }
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
