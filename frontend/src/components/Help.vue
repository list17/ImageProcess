<template>
  <div>
    <el-row type="flex" justify="center">
      <el-col :span="18">
        <el-card class="box-card">
          <div style="font-size: 30px;">
            GStrategy-帮助
          </div>
        </el-card>
      </el-col>
    </el-row>



    <el-row type="flex" justify="center">
       <el-col :span="18">
        <el-card class="box-card">
          <div style="margin-bottom: 20px; color: #606266; padding: 0 50px 0 0; font-weight: bold;">
            简介
          </div>
          <div style="font-size: 16px">
            <p>这是一个收集道具抵达终点，并在地图中使用各种技能加速自己的收集过程以及阻碍对方收集过程的游戏。</p>
            <p>在有限的步数内尽可能多的将道具放入存储槽中以获得更高的分数。不同道具分数不同，同一道具与不同槽的匹配度也不同，双方共同决定了将道具放入槽后的最终得分。</p>
            <p>玩家的程序将在每一步开始时接受当前地图的信息，然后在规定的计算时间内计算出这一步自己要进行什么操作（包括移动、拾取放下和释放技能等），如果程序输出非法操作或运行超时，则会被视为放弃本步甚至被判负。</p>
            <p>详细信息见文档，同时，你需要下载可视化文件并按其中的提示文档利用可视化为你的程序debug</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row type="flex" justify="center">
      <el-col :span="18">
        <el-card class="box-card">
            <el-col :span="18">
              <div style="margin-bottom: 20px; color: #606266; padding: 0 50px 0 0; font-weight: bold;">
                游戏文件
              </div>
            </el-col>
            <el-col :span="4">
              <el-button @click="downloadReplay(id)" size="small">可视化文件下载</el-button>
            </el-col>
        </el-card>  
      </el-col>
    </el-row>

     <el-row type="flex" justify="center">
       <el-col :span="18">
        <el-card class="box-card">
          <el-col :span="14">
              <div style="margin-bottom: 20px; color: #606266; padding: 0 50px 0 0; font-weight: bold;">
                文档下载
              </div>
            </el-col>
            <el-col :span="4">
              <el-button @click="downloadPDF(fileid1)" size="small">.pdf文件下载</el-button>
            </el-col>
            <el-col :span="4">
              <el-button @click="downloadMD(fileid2)" size="small">.md文件下载</el-button>
          </el-col>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        id:"可视化.zip",
	      fileid1:"游戏文档.pdf",
	      fileid2:"游戏文档.md",
      }
    },  
  methods: {
    downloadReplay(matchid){
      let url = '/api/game/file_download/' + matchid ;
      window.open(url,'_blank');
    },
    downloadPDF(id){
      let url = '/api/game/file_download/' + id;
      window.open(url,'_blank');
    },
    downloadMD(id){
      let url = '/api/game/file_download/' + id;
      window.open(url,'_blank');
    },
  },
}
</script>

<style scoped>
  .box-card {
    border-radius: 10px;
  }
  .el-row:first-child {
    margin-top: 20px;
    margin-bottom: 40px;
    }
  .el-row {
    margin-bottom: 10px;
  }
  dd {
    font-size: small;
    color: #606266;
    padding-top: 10px;
  }
</style>
