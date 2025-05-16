package configuration;

import org.springframework.amqp.core.*;
import org.springframework.context.annotation.*;

@Configuration
public class RabbitConfig {
    @Bean
    public DirectExchange exchange() {
        return new DirectExchange("catalogue.exchange");
    }

    @Bean
    public Queue queue() {
        return new Queue("order.creation.queue", false);
    }

    @Bean
    public Binding binding(Queue queue, DirectExchange exchange) {
        return BindingBuilder.bind(queue).to(exchange).with("product.created");
    }
}
