import { InputValues } from '@/components/InputValues'
import { Context } from '@/context/Context'
import React, { useContext } from 'react'
import ForwardGraph from '@/components/ForwardPlotGraph'

export default function NewPlotting() {
  const { forward_r1, forward_r2, forward_lambda1, backward_r1, backward_r2, backward_lambda1, type, theta, time } = useContext(Context)

  return (
    <div className=" min-h-screen  text-white">
      <div className="w-screen mx-auto  rounded-lg my-8 p-8">
    
        {/* <SelectComponent /> */}
        <InputValues />
          <div>
            <div className='!text-white'>
              <ForwardGraph
                forward_r1={forward_r1}
                forward_r2={forward_r2}
                forward_lambda1={forward_lambda1}
                backward_r1={backward_r1}
                backward_r2={backward_r2}
                backward_lambda1={backward_lambda1}
              />
            </div>
            
          </div>
        {/* {type === "ThetavsT" && <ThetavsT xValues={time} yValues={theta} />} */}
      </div>
    </div>
  )
}