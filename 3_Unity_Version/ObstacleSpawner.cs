using UnityEngine;

public class ObstacleSpawner : MonoBehaviour
{
    public GameObject cloudPairPrefab;
    public float spawnRate = 2f;
    private float timer = 0f;

    void Update()
    {
        timer += Time.deltaTime;
        if (timer > spawnRate)
        {
            SpawnCloud();
            timer = 0;
        }
    }

    void SpawnCloud()
    {
        float randomY = Random.Range(-2f, 2f);
        Instantiate(cloudPairPrefab, new Vector3(10, randomY, 0), Quaternion.identity);
    }
}