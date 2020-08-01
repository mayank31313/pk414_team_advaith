<template>
<q-page>
<div v-if="recommendedCrop" class="text-center q-mb-md" >
        <q-img src="statics/kg.png" width="50%"  class="q-mt-sm">
        </q-img><br><br>
        <label class="text-h5  text-weight-normal">It is recommended that you should  grow {{ recommendedCrop.recommended[0].crop_name }}</label>
<!-- <q-table
     virtual-scroll
     hide-pagination
     hide-bottom
     hide-header
     pagination="false"
     bordered
      class="my-sticky-header-table"
      title="Recommended Crops"
      :data="recommendedCrop.recommendations"
      :row-key="recommendedCrop.recommendations.length"
    /> -->
</div>
<q-table
  title="Recommended Crops"
  :data="recommendedCrop.recommendations"
  :columns="columns"

/>
</q-page>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
  data () {
    return { 
      columns:[
        {name:'crop_name'},
        {name:'confidence'}
      ]
    }
  },
  computed:{
    ...mapGetters('store',['recommendedCrop']),
    }
  }
</script>
<style lang="sass">

</style>