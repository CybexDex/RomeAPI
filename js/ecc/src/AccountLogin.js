const PrivateKey = require("./PrivateKey");

const normalize_brainKey = function (brainKey) {
    if (!(typeof brainKey === 'string')) {
        throw new Error("string required for brainKey");
    }

    brainKey = brainKey.trim();
    return brainKey.split(/[\t\n\v\f\r ]+/).join(' ');
}

const generateKeys = function (accountName, password, role = "active") {

    if (!accountName || !password) {
        throw new Error("Account name or password required");
    }
    if (password.length < 12) {
        throw new Error("Password must have at least 12 characters");
    }

    let seed = accountName + role + password;
    return PrivateKey.fromSeed(normalize_brainKey(seed));

}

// const checkKeys = function ({accountName, password, auths}) {
//     if (!accountName || !password || !auths) {
//         throw new Error("checkKeys: Missing inputs");
//     }
//     let hasKey = false;
//
//     for (let role in auths) {
//         let {privKeys, pubKeys} = this.generateKeys(accountName, password, [role]);
//         auths[role].forEach(key => {
//             if (key[0] === pubKeys[role]) {
//                 hasKey = true;
//                 this.set(role, {priv: privKeys[role], pub: pubKeys[role]});
//             }
//         });
//     };
//
//     return hasKey;
// }

exports.generateKeys = generateKeys;
