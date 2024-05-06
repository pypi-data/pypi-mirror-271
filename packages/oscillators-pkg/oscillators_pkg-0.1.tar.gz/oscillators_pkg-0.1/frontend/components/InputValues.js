"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { useContext, useState } from "react"
import { Button } from "@/components/ui/button"
import axios from 'axios'
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Context } from "@/context/Context"

const formSchema = z.object({
    username: z.string().min(2, {
        message: "Username must be at least 2 characters.",
    }),
})

const LoadingOverlay = ({ isLoading }) => {
    return isLoading ? (
        <div className="fixed inset-0 flex items-center justify-center z-50">
            <div className="bg-black bg-opacity-50 inset-0 fixed" />
            
        </div>
    ) : null;
};

export function InputValues() {
    const form = useForm()
    const { setforward_r1, setforward_r2, setbackward_r1, setbackward_r2, setforward_lambda1, setbackward_lambda1, type, settype, settheta, settime } = useContext(Context)
    const [isLoading, setIsLoading] = useState(false);

    const onSubmit = (e) => {
        const formData = form.getValues();
        const convertedData = {};
        for (const key in formData) {
            convertedData[key] = parseFloat(formData[key]);
        }

        if (type === "Polar" && (activity.length !== 0)) {
            localStorage.setItem('time', parseInt(formData.time))
            setTime(parseInt(formData.time));
        } else {
            setIsLoading(true); 

            console.log(convertedData);
            try {
                let url;
                url = "http://127.0.0.1:8000/api/v1/oscillators/"
                if(type == "ThetavsT"){
                    url = "http://127.0.0.1:8000/api/v1/__get__theta__vs__t__values__/"
                }
                axios.post(url, convertedData)
                    .then((response) => {
                        const data = response.data;
                        console.log(data)

                            setforward_r1(data.r1_values_forward)
                            setforward_lambda1(data.k1_values_forward)
                            setbackward_r1(data.r1_values_backward)
                            setbackward_lambda1(data.k1_values_backward)

                        if (type == "ThetavsT") {
                            settheta(data.theta)
                            settime(data.time)
                        }
                    })
                    .catch((error) => {
                        console.error('Error running Fortran code:', error);
                    })
                    .finally(() => {
                        setIsLoading(false); // Set loading state to false after API call completes
                    });
            } catch (error) {
                console.error('Error running Fortran code:', error);
                setIsLoading(false); // Set loading state to false in case of an error
            }
        }
    };

    return (
        <div className="text-black">
            <LoadingOverlay isLoading={isLoading} />
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="max-w-3xl mx-auto">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                        
                            <div>
                                <FormField
                                    control={form.control}
                                    name="n"
                                    render={({ field }) => (
                                        <FormItem className="mb-6">
                                            <FormLabel className="text-white">Number of Oscillators</FormLabel>
                                            <FormControl>
                                                <Input placeholder="Number of Oscillators" {...field} className="w-full" />
                                            </FormControl>
                                            
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>
                        

                        
                            <div>
                                <FormField
                                    control={form.control}
                                    name="k1_start"
                                    render={({ field }) => (
                                        <FormItem className="mb-6">
                                            <FormLabel className="text-white">Coupling Start Value</FormLabel>
                                            <FormControl>
                                                <Input placeholder="Coupling Start Value" {...field} className="w-full" />
                                            </FormControl>
                                            
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>
                        

                        
                            <div>
                                <FormField
                                    control={form.control}
                                    name="k1_end"
                                    render={({ field }) => (
                                        <FormItem className="mb-6">
                                            <FormLabel className="text-white">Coupling End Value</FormLabel>
                                            <FormControl>
                                                <Input placeholder="Coupling End Value" {...field} className="w-full" />
                                            </FormControl>
                                            
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>
                        

                        {type === "ThetavsT" && (
                            <div>
                                <FormField
                                    control={form.control}
                                    name="k1"
                                    render={({ field }) => (
                                        <FormItem className="mb-6">
                                            <FormLabel className="text-white">Coupling Strength 1</FormLabel>
                                            <FormControl>
                                                <Input placeholder="Coupling Strength 1" {...field} className="w-full" />
                                            </FormControl>
                                           
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>
                        )}

                        
                            <div>
                                <FormField
                                    control={form.control}
                                    name="k2"
                                    render={({ field }) => (
                                        <FormItem className="mb-6">
                                            <FormLabel className="text-white">Coupling Strength 2</FormLabel>
                                            <FormControl>
                                                <Input placeholder="Coupling Strength 2" {...field} className="w-full" />
                                            </FormControl>
                                            
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>
                    

                        
                    </div>
                    <div className="flex justify-center mt-2">
                        <Button type="submit">Submit</Button>
                    </div>
                </form>
            </Form>
        </div>
    )
}