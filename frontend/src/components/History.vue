<template>
<div>
    <el-table :data="dataset" highlight-current-row style="width: 70%; margin:0 auto;">
        <el-table-column prop="id" label="ID" min-width="5%" >
        </el-table-column>
        <el-table-column prop="feature" label="进行的操作" min-width="10%" >
        </el-table-column>
        <el-table-column label="图片" min-width="40%" >
            <template slot-scope="scope" style="display:flex;justify-content:space-around ;">
                <div style="display:flex; justify-content:space-between; width:100%;height:200px">
                    <div style="width:100%;height:200px">
                        <div>处理前</div>
                        <img :src="scope.row.image[0]"  width=90% />
                    </div>
                    <div style="width:100%;height:200px">
                        <div>处理后</div>
                        <img :src="scope.row.image[1]" width=90% />
                    </div>
                </div>
            </template>
        </el-table-column>
        <el-table-column label="下载该次图片" min-width="10%">
            <template slot-scope="scope">
                <el-button size="small" @click="handleEdit(scope.row)">下载</el-button>
            </template>
        </el-table-column>
    </el-table>
</div>
</template>

<script>
  export default {
    name:'history',
    components:{

    },
    data() {
      return {
          dataset:[]
      }
    },
    mounted() {
        this.$axios.post('/filetransfer/download_user_history').then((response)=>{
            this.dataset = response.data.dataset;
        })
    },
    methods: {
        handleEdit(index){
            console.log(index)
            window.open(index['image'][1],'_blank');
        },
        forceFileDownload(response){
            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', 'file.png') //or any other extension
            document.body.appendChild(link)
            link.click()
        }
    }
  }

</script>

<style scoped>

</style>
