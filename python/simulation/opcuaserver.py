from asyncua import Server, ua
import asyncio

async def main():
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/siemens/trafficcontroller/")
    
    # Siemens-style namespace
    uri = "http://siemens.com/trafficcontroller"
    idx = await server.register_namespace(uri)

    # Create Traffic Controller Object
    traffic_controller = await server.nodes.objects.add_object(idx, "TrafficController")

    # Traffic Light States (Boolean)
    red_light = await traffic_controller.add_variable(idx, "RedLight", True, ua.VariantType.Boolean)
    yellow_light = await traffic_controller.add_variable(idx, "YellowLight", False, ua.VariantType.Boolean)
    green_light = await traffic_controller.add_variable(idx, "GreenLight", False, ua.VariantType.Boolean)

    # Pedestrian Button Pressed (Boolean)
    pedestrian_button = await traffic_controller.add_variable(idx, "PedestrianButton", False, ua.VariantType.Boolean)

    # Cycle Timer (Int32)
    cycle_timer = await traffic_controller.add_variable(idx, "CycleTimer", 0, ua.VariantType.Int32)

    # Error State (String)
    error_state = await traffic_controller.add_variable(idx, "ErrorState", "", ua.VariantType.String)

    # Make variables writable
    for var in [red_light, yellow_light, green_light, pedestrian_button, cycle_timer, error_state]:
        await var.set_writable()

    # Simulate traffic light cycle
    async with server:
        while True:
            await red_light.write_value(True)
            await yellow_light.write_value(False)
            await green_light.write_value(False)
            await cycle_timer.write_value(5)
            await asyncio.sleep(5)

            await red_light.write_value(False)
            await yellow_light.write_value(True)
            await cycle_timer.write_value(2)
            await asyncio.sleep(2)

            await yellow_light.write_value(False)
            await green_light.write_value(True)
            await cycle_timer.write_value(5)
            await asyncio.sleep(5)

            await green_light.write_value(False)
            await yellow_light.write_value(True)
            await cycle_timer.write_value(2)
            await asyncio.sleep(2)

            await yellow_light.write_value(False)

if __name__ == "__main__":
    asyncio.run(main())