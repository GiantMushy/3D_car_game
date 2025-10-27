public class D6 {
    FloatBuffer vertexBuffer;
    FloatBuffer texCoordBuffer;
    Texture texture;

    public D6(Texture tex)
    {
        vertexBuffer = BufferUtils.newFloatBuffer(72);
        vertexBuffer.put(new float[] {
            -0.5f, -0.5f, -0.5f, -0.5f, 0.5f, -0.5f,
            0.5f, -0.5f, -0.5f, 0.5f, 0.5f, -0.5f,
            0.5f, -0.5f, -0.5f, 0.5f, 0.5f, -0.5f,
            0.5f, -0.5f, 0.5f, 0.5f, 0.5f, 0.5f,
            0.5f, -0.5f, 0.5f, 0.5f, 0.5f, 0.5f,
            -0.5f, -0.5f, 0.5f, -0.5f, 0.5f, 0.5f,
            -0.5f, -0.5f, 0.5f, -0.5f, 0.5f, 0.5f,
            -0.5f, -0.5f, -0.5f, -0.5f, 0.5f, -0.5f,
            -0.5f, 0.5f, -0.5f, -0.5f, 0.5f, 0.5f,
            0.5f, 0.5f, -0.5f, 0.5f, 0.5f, 0.5f,
            -0.5f, -0.5f, -0.5f, -0.5f, -0.5f, 0.5f,
            0.5f, -0.5f, -0.5f, 0.5f, -0.5f, 0.5f
        });
        vertexBuffer.rewind();


        texCoordBuffer = BufferUtils.newFloatBuffer(48);
        texCoordBuffer.put(new float[] {
            // Front face (1 dot) - center cell (2,2)
            0.333f, 0.333f, 0.333f, 0.667f, 0.667f, 0.333f, 0.667f, 0.667f,
            
            // Right face (2 dots) - left-middle cell (1,2)
            0.0f, 0.333f, 0.0f, 0.667f, 0.333f, 0.333f, 0.333f, 0.667f,
            
            // Back face (3 dots) - top-middle cell (2,1)
            0.333f, 0.0f, 0.333f, 0.333f, 0.667f, 0.0f, 0.667f, 0.333f,
            
            // Left face (4 dots) - bottom-middle cell (2,3)
            0.333f, 0.667f, 0.333f, 1.0f, 0.667f, 0.667f, 0.667f, 1.0f,
            
            // Top face (5 dots) - right-middle cell (3,2)
            0.667f, 0.333f, 0.667f, 0.667f, 1.0f, 0.333f, 1.0f, 0.667f,
            
            // Bottom face (6 dots) - top-right cell (3,1)
            0.667f, 0.0f, 0.667f, 0.333f, 1.0f, 0.0f, 1.0f, 0.333f
        });
        texCoordBuffer.rewind();


    }

    public void draw()
    {
        Gdx.gl11.glVertexPointer(3, GL11.GL_FLOAT, 0, vertexBuffer);

        // Enable texture coordinates and bind texture
        Gdx.gl11.glEnableClientState(GL11.GL_TEXTURE_COORD_ARRAY);
        Gdx.gl11.glTexCoordPointer(2, GL11.GL_FLOAT, 0, texCoordBuffer);
        texture.bind();


        Gdx.gl11.glNormal3f(0.0f, 0.0f, -1.0f);
        Gdx.gl11.glDrawArrays(GL11.GL_TRIANGLE_STRIP, 0, 4);
        Gdx.gl11.glNormal3f(1.0f, 0.0f, 0.0f);
        Gdx.gl11.glDrawArrays(GL11.GL_TRIANGLE_STRIP, 4, 4);
        Gdx.gl11.glNormal3f(0.0f, 0.0f, 1.0f);
        Gdx.gl11.glDrawArrays(GL11.GL_TRIANGLE_STRIP, 8, 4);
        Gdx.gl11.glNormal3f(-1.0f, 0.0f, 0.0f);
        Gdx.gl11.glDrawArrays(GL11.GL_TRIANGLE_STRIP, 12, 4);
        Gdx.gl11.glNormal3f(0.0f, 1.0f, 0.0f);
        Gdx.gl11.glDrawArrays(GL11.GL_TRIANGLE_STRIP, 16, 4);
        Gdx.gl11.glNormal3f(0.0f, -1.0f, 0.0f);
        Gdx.gl11.glDrawArrays(GL11.GL_TRIANGLE_STRIP, 20, 4);
        
    }
}

public class coords {
    public float x;
    public float y;
    public float z;
}
public class RolledD6 {
    public float size;
    public coords position;
    public coords rotationAxis;
    public float rotationAngle;
}

void drawDiceSet() {
    List<RolledD6> diceList = DiceRollingEngine.getDice();
    foreach(RolledD6 d in diceList) {
        // Save current matrix state
        Gdx.gl11.glPushMatrix();
        
        // Translate to the dice position
        Gdx.gl11.glTranslatef(d.position.x, d.position.y, d.position.z);
        
        // Rotate around the specified axis by the specified angle
        Gdx.gl11.glRotatef(d.rotationAngle, d.rotationAxis.x, d.rotationAxis.y, d.rotationAxis.z);
        
        // Scale to the specified size
        Gdx.gl11.glScalef(d.size, d.size, d.size);
        
        // Draw the dice
        dice.draw();
        
        // Restore matrix state
        Gdx.gl11.glPopMatrix();
    }
}