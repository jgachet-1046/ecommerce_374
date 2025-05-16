package controller;

import model.Product;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import repository.ProductRepository;

import java.util.List;

@RestController
@RequestMapping("/api/products")
public class ProductController {

    @Autowired
    private ProductRepository repo;

    @Autowired
    private org.springframework.amqp.rabbit.core.RabbitTemplate rabbitTemplate;

    @GetMapping
    public List<Product> getAll() {
        return repo.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Product> getById(@PathVariable Long id) {
        return repo.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Product> create(@RequestBody Product product) {
        Product saved = repo.save(product);
        rabbitTemplate.convertAndSend("catalogue.exchange", "product.created", saved.getId());
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }
}
