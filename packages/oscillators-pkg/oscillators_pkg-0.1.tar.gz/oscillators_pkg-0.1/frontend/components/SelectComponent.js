import * as React from "react"

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useContext } from "react"
import { Context } from "@/context/Context"

export function SelectComponent() {
  const {type,settype} = useContext(Context)
  return (
    <div className="flex justify-center items-center my-10">
      <Select onValueChange={(e)=>{
        alert(e)
        settype(e)
      }}>
        <SelectTrigger className="w-[180px] text-black">
          <SelectValue placeholder="Select a Graph" />
        </SelectTrigger>
        <SelectContent>
          <SelectGroup>
            <SelectItem value="Forward">Forward Graph</SelectItem>
            <SelectItem value="ThetavsT">ThetavsT Graph</SelectItem>
            <SelectItem value="Backward">Backward Graph</SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>
    </div>
  )
}
