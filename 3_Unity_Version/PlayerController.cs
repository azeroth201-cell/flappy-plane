using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float lift = 300f;
    private Rigidbody2D rb;
    private bool isAlive = true;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        if (isAlive && Input.GetMouseButtonDown(0))
        {
            rb.velocity = Vector2.up * lift;
        }
    }

    void OnCollisionEnter2D(Collision2D col)
    {
        if (col.gameObject.CompareTag("Obstacle"))
        {
            isAlive = false;
            // Добавь вызов Game Over UI
        }
    }
}