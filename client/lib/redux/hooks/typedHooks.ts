import type { AppStore,RootState,AppDispatch } from "@/lib/redux/store";
import type {TypedUseSelectorHook} from "react-redux";
import { UseDispatch,useSelector,useStore,useDispatch } from "react-redux";

export const useAppDispatch: ()=> AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
export const useAppStore: ()=> AppStore = useStore;
