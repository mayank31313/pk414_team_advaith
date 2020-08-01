import axios from 'axios'
import Vue from 'vue'
import { Notify } from 'quasar'
import  { firebaseDb } from 'src/boot/firebase'

let url = 'http://10.8.0.10:8000/api/'
let messageRef

const state={
  userDetails:{},
  messages : {},
  users:{},
  recommendedCrop:{}
}
const mutations={
  setUserDetails(state,payload){
    state.userDetails = payload
  },
  addMessages(state,payload){
    Vue.set(state.messages, payload.messageId, payload.messageDetails)
  },
  addAllUsers(state,payload){
    Vue.set(state.users, payload.userid, payload.user)
  },
  clearMessages(state){
    state.messages = {}
  },
  removeAllUsers(state){
    state.users = {}
  },
  setRecommendedCrop(state, payload){
    state.recommendedCrop = payload
  }
}
const actions={
    registerUser({ dispatch },payload){
      return axios.post(url+'register/',{
                                        "name":payload.name,
                                        "pincode":payload.pincode,
                                        "city":payload.city,
                                        "username":payload.phone,
                                        "password":payload.password
                                    }
      ,{ headers: {
        'content-type': 'application/json'
        }})
      .then(response => {
        payload.click=false
        if(response.status == 200){
          window.localStorage.setItem('username',payload.phone)
          payload.click=false
          Notify.create({
            type: 'positive',
            message: `Account Created Successfully ! `,
            actions: [
            { label: 'OK', color: 'white', handler: () => { /* ... */ } }
          ],
            position:'center'
          })
          window.localStorage.setItem('token',response.data.token)
          dispatch('handleUserdetails')
          this.$router.push('/home')
          location.reload()
        }
      })
      .catch(error => {
        console.log(error.response)
      })  

  },
  Production({},payload){
    return axios.post(url+'production')

  },
  PricePrediction({},payload){
    return axios.get(url+'price/',payload)
    .then(response => {
      console.log(response)
      // if(response.status == 200){
      //   for (let i=0;i<=response.data.length;i++){
      //       payload.data.push(response.data[i])
      //   }
    
      // }
    })
},
loginUser({ dispatch },payload){
    return axios.post(url+'login/',{
                                      "username":payload.phone,
                                      "password":payload.password
                                  }
    ,{ headers: {
      'content-type': 'application/json'
      }})
    .then(response => {
      if(response.status == 200){
        window.localStorage.setItem('username',payload.phone)
        payload.click=false
        window.localStorage.setItem('token',response.data.token)
        dispatch('handleUserdetails')
        if(payload.username === '0000000000'){
          this.$router.push('/admin')
        }else{
          this.$router.push('/home')}
        location.reload()
      }
    })
    .catch(error => {
      console.log(error.response)
    })  

},
handleUserDetails( { commit }){
  let username = window.localStorage.getItem('username')
  return axios.get(url+'user/?username='+username)
  .then(response =>{
    if (response.status == 200){
      console.log('userDetails : ',response.data[0])
      if(username==='0000000000'){
        let users = response.data
        for (let i = 0; i < response.data.length; i++) {
          if (response.data[i].id=='3'){
            let userDetails = response.data[i]
            commit('setUserDetails', { userDetails })
          }
          else{
              commit('addAllUsers', { 
                userid:response.data[i].id,
                user:{
                  name:response.data[i].name,
                  username:response.data[i].username,
                  city:response.data[i].city,
                  pincode:response.data[i].pincode
                }
              })
            }
        }
      }else{
        let userDetails = response.data[0]
        commit('setUserDetails', { userDetails })
      }
    }
  } )
  .catch(error => {
    console.log(error.response)
  })
},
cropRecommend( { commit },payload){
  console.log(payload)
  return axios.post(url+'crop/',payload)
    .then(response => {
    if(response.status == 200){
      console.log(response.data);
      commit('setRecommendedCrop', response.data)
      this.$router.push('/output')
    }
    })
    .catch(error => {
    console.log(error.response)
    })  
},

logoutUser({ commit }){
  if(window.localStorage.getItem('username')==='0000000000'){
    commit('removeAllUsers')
  }
  window.localStorage.removeItem('token')
  window.localStorage.removeItem('username')
  commit('setUserDetails',{})
  location.reload()
  this.$router.push('/')
},

// Chat related methods

 firebaseGetMessages({ state, commit }, payload){
   let userId = state.userDetails.userDetails.id
   messageRef = firebaseDb.ref('chats/'+userId+'/'+payload)
    messageRef.on(
      'child_added', snapshot => {
        let messageDetails = snapshot.val()
        let messageId = snapshot.key
        commit('addMessages',{
          messageId:messageId,
          messageDetails:messageDetails
        })
      })
 },
 firebaseStopGettingMessages({commit}){
   if(messageRef){
     messageRef.off('child_added')
     commit('clearMessages')
   }
 },
 firebaseSendMessage({},payload){
   let userId = state.userDetails.userDetails.id
    firebaseDb.ref('chats/' +userId+'/'+
    payload.otheruserid).push(payload.message)

    payload.message.from = "them"

    firebaseDb.ref('chats/' +payload.otheruserid+'/'+
    userId).push(payload.message)
 }
} 
const getters={
    users: state => {
      return state.users;
    },
    recommendedCrop: state =>{
      return state.recommendedCrop
    }
}
export default{
    namespaced:true,
    state,
    mutations,
    actions,
    getters,
}