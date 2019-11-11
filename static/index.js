document.addEventListener("keypress", function(event) {
    if (event.keyCode == 13) {

      new Promise((resolve, reject) => {
          url = "http://localhost:5000/test";
          (async () => {
            const resp = await fetch(url, {
              method: 'POST',
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({data: "hello"})
            }).then((resp) => {
              return resp.json();
            }).then((data) => {
              if (data["data"] == 'success') {resolve()}
              finalResp = JSON.stringify(data);
              console.log(finalResp);
            });
          })();
      });

    }
})

class promise {
  constructor(i) {
    this.pending = true;
    this.promise = new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve();
      }, (10-i)*1000);
    }).then(()=> {
      if (i == 0 || promises[i-1].pending==false) {
        promises[1].targetProxy.pending = false;
        console.log(i);
      }
    });
  }
}
promises = new Array(10).fill().map((e,i) => {
  return new promise(i);
});
promises.forEach((promise, i)=> {
  if (i > 0) {
    promise.targetProxy = new Proxy(promises[i-1], {
      set: function (target, key, value) {
          console.log(`${key} set to ${value}`);
          console.log(i)
          target[key] = value;

          //for example proxy of 1 changes 0 and then calls proxy of 2 which changes 1 and then calls 3.....

          promises[i+1].targetProxy.pending = false;
          return true;
      }
    });
  }
});



// this.handler = {
//   set(obj, prop, value) {
//     if (prop == 'pending' && value==false) {
//       console.log('works');
//     } else {
//       return Reflect.set(...arguments);
//     }
//   }
// }
// this.proxy = new Proxy(promises[i-1], this.handler);
// this.proxy = new Proxy(promises[i-1], {
//   set: (target, key, value)=>{
//     console.log(`${key} set to ${value}`);
//     return true;
//   }
// });


// class lol {
//   constructor() {
//     this.dick = 19;
//   }
// };
// mylol = new lol();
//
//
// class nigga {
//   constructor() {
//      this.targetProxy = new Proxy(mylol, {
//       set: function (target, key, value) {
//           console.log(`${key} set to ${value}`);
//           target[key] = value;
//           return true;
//       }
//     });
//   }
// }
//
//
// mynigga = new nigga();
// mynigga.targetProxy.dick = 18;
// //expected output: dick set to 18
