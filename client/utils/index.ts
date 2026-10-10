import InitiateSocialAuth from "./initiateSocialAuth";

export {default as extractErrorMessage} from "./extractErrorMessage";
export {default as PersistAuth} from "./PersistAuth";


export const UseGoogle = ()=>{
    console.log("[UseGoogle] called");
    InitiateSocialAuth("google-oauth2","google")
};
export {formatDate } from "./formatDate";
export {capitalizeFirstLetter } from "./capitalizeFirstLetter";
export {getViewText } from "./getViewText";
export {getRepliesText } from "./getRepliesText";
export {sortByDateDescending } from "./sortByDate";