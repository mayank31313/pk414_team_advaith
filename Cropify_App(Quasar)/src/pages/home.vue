<template>
<q-page >
    <div class="q-ml-lg q-mt-md text-weight-medium" style="font-size:20px">Latest news</div>
    <div class="q-pa-xs flex full-width justify-center">
    <div class="full-width q-gutter-sm">
      <q-intersection
        v-for="feed in feeds"
        :key="feed.id"
        transition="flip-right"
      >
        <q-item clickable v-ripple>
          <q-item-section avatar class="full-width">
            <q-img no-default-spinner v-bind:src="feed.img" />          
            <q-item-label class="q-mt-sm text-justify text-subtitle2">{{ feed.title }}</q-item-label>
            <q-item-label caption lines="5" class="text-justify">{{ feed.des }}</q-item-label>
          </q-item-section>
          
        </q-item>
        <q-separator inset />
      </q-intersection>
      
    </div>
  </div>
</q-page>
</template>
<script>
export default {
    created(){
    let token = window.localStorage.getItem('token')
    let username = window.localStorage.getItem('username')
    if(!token){
      this.$router.push('/')
    }else if(username==='0000000000'){
      this.$router.push('/admin')
    }
  },
    data(){
        return{
            username:window.localStorage.getItem('username'),
            feeds:[
                {   
                    "id":1,
                    "img":"https://img.etimg.com/thumb/msid-77167633,width-160,height-120,imgsize-134210/saffron-grown-in-kashmir-gets-geographical-indication-certification.jpg",
                    "title":"Saffron grown in Kashmir gets Geographical Indication certification",
                    "des":"Soon after taking over as lieutenant governor, Girish Chander Murmu took a personal interest in ensuring that Kashmir saffron gets GI certification."
                },
                {   
                    "id":2,
                    "img":"https://img.etimg.com/thumb/msid-77076975,width-160,height-120,imgsize-804117/festive-bonus-negotiation-in-tea-plantation-for-2020-is-likely-to-generate-extra-warmth-.jpg",
                    "title":"Festive Bonus negotiation in tea plantation for 2020 is likely to generate extra warmth.",
                    "des":"Worker's festival bonus is likely to come up as a major issue of conflict in the labour intensive tea plantation sector. While financially hit workers will press harder for higher bonus, accepting that will be too tough for the planters, equal victims of the pandemic situation."
                },
                {   
                    "id":3,
                    "img":"https://img.etimg.com/thumb/msid-77066189,width-160,height-120,imgsize-628516/soybean-crop-needs-rain-in-a-week-otherwise-yields-will-fall-says-trade-body.jpg",
                    "title":"Soybean crop needs rain in a week, otherwise yields will fall, says trade body.",
                    "des":"area due to poor germination of seeds that were sowed the first time. Crop condition is normal but rainfall is needed in the next 5 to 7 days in some parts of Latur, Osmanabad and Beed districts, failing which crop may be affected due to moisture stress, a SOPA release said."
                },
                {   
                    "id":4,
                    "img":"https://img.etimg.com/thumb/msid-77033044,width-160,height-120,imgsize-320910/heavy-monsoon-rains-speed-up-crop-planting-in-india.jpg",
                    "title":"Heavy monsoon rains speed up crop planting in India.",
                    "des":"Farmers typically start planting their summer-sown crops June 1, when monsoon rains usually reach India. Planting usually continues until the end of July or early August."
                },
                {   
                    "id":5,
                    "img":"https://img.etimg.com/thumb/msid-77021422,width-160,height-120,imgsize-1075412/no-impact-of-covid-19-pandemic-on-kharif-sowing-acreage-up-21-20-so-far-government.jpg",
                    "title":"No impact of COVID-19 pandemic on kharif sowing; acreage up 21.20% so far: Government.",
                    "des":"The country has so far received good rainfall and water level in 123 reservoirs across the country is in good position, it said in the latest sowing data. Sowing of kharif crops begins with the onset of southwest monsoon from June, while harvesting starts from October. Rice is the main kharif crop, besides bajra, arhar, urad,"
                },
                {   
                    "id":6,
                    "img":"https://img.etimg.com/thumb/msid-76893489,width-300,imgsize-189631,,resizemode-4,quality-100/wheat-bccl.jpg",
                    "title":"Government's wheat procurement touches record high of 38.98 million tonnes so far in 2020-21.",
                    "des":"We have procured 38.98 million tonnes of wheat so far. The procurement operations are almost complete in major states. Few thousand tonnes more will be brought in the next few days,a senior FCI official told ."
                },



            ]
        }
    }
}
</script>