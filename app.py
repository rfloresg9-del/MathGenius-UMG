import random
import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

st.set_page_config(page_title='MathGenius UMG', page_icon='📐', layout='wide')
st.markdown('''<style>.block-container{padding-top:2rem;max-width:1200px}h1,h2,h3{color:#2156a5}div[data-testid="stMetric"]{border:1px solid #ccd8ef;border-radius:12px;padding:12px}</style>''',unsafe_allow_html=True)
x=sp.Symbol('x',real=True)
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)
ALLOWED={'x':x,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'sqrt':sp.sqrt,'exp':sp.exp,'log':sp.log,'ln':sp.log,'abs':sp.Abs,'pi':sp.pi,'E':sp.E}

def parse(s):
    if not s or len(s)>180: raise ValueError('Ingresa una expresión de máximo 180 caracteres.')
    if any(c in s for c in ['__','[',']','{','}',';',':','\\']): raise ValueError('La expresión contiene caracteres no permitidos.')
    import re
    names=re.findall(r'[A-Za-z_]+',s)
    if any(n not in ALLOWED for n in names): raise ValueError('Usa x, números y funciones permitidas (sin, cos, sqrt, exp, log).')
    value=parse_expr(s,local_dict=ALLOWED,global_dict={'Integer':sp.Integer,'Float':sp.Float,'Rational':sp.Rational,'Symbol':sp.Symbol,'Function':sp.Function,'Pow':sp.Pow,'Add':sp.Add,'Mul':sp.Mul},transformations=TRANS,evaluate=True)
    if value.free_symbols-{x}:raise ValueError('Solo se admite la variable x.')
    return value

def show(label,v):
    st.markdown('**'+label+'**')
    st.latex(sp.latex(v))

def safe(call):
    try:call()
    except (ValueError,TypeError,ZeroDivisionError,sp.SympifyError,NotImplementedError) as e:st.error(f'No se pudo resolver: {e}')
    except Exception:st.error('No se pudo resolver este caso. Comprueba la expresión e intenta con una función elemental.')

st.title('📐 MathGenius UMG')
st.caption('Asistente virtual de Cálculo y Precálculo · Universidad Mariano Gálvez de Guatemala')

with st.sidebar:
    st.header('Información académica')

    st.write('**Universidad:** Mariano Gálvez de Guatemala')
    st.write('**Proyecto:** MathGenius UMG')

    st.write('**Integrantes:**')
    st.write('1. Richard Alexander Flores Gramajo')
    st.write('2. Mario David Guerra Sazo')

    st.write('**Sección:** B')
    st.write('**Asignatura:** Cálculo y Precálculo')

    st.info(
        'Escribe potencias como x^2, '
        'multiplicaciones como 2*x '
        'y funciones como sin(x).'
    )

    st.write('**Asignatura:** Cálculo y Precálculo')
    st.info('Escribe potencias como x^2, multiplicaciones como 2*x y funciones como sin(x).')

sections=['Álgebra y funciones','Gráficas','Límites','Derivadas','Integrales','Aplicaciones','Ejemplos y práctica']
tab=st.tabs(sections)
with tab[0]:
    st.subheader('Álgebra y funciones')
    mode=st.selectbox('Operación',['Resolver ecuación','Factorizar','Dominio y rango','Composición f(g(x))'],key='alg')
    f=st.text_input('Expresión f(x) o lado izquierdo de la ecuación',value='x^2-5*x+6',key='af')
    rhs=st.text_input('Lado derecho de la ecuación',value='0') if mode=='Resolver ecuación' else None
    g=st.text_input('g(x)',value='x+1') if mode=='Composición f(g(x))' else None
    if st.button('Resolver álgebra'):
        def solve_alg():
            F=parse(f);show('Dato de entrada:',F)
            if mode=='Resolver ecuación':
                R=parse(rhs);show('Ecuación:',sp.Eq(F,R,evaluate=False));show('Paso 1: llevar todo a cero:',sp.Eq(sp.factor(F-R),0,evaluate=False))
                roots=sp.solveset(F-R,x,domain=sp.S.Reals);show('Paso 2: conjunto solución real:',roots)
                if isinstance(roots,sp.FiniteSet):
                    for r in roots:show('Verificación por sustitución:',sp.Eq(sp.simplify((F-R).subs(x,r)),0))
            elif mode=='Factorizar':show('Resultado factorizado:',sp.factor(F));show('Verificación al expandir:',sp.expand(sp.factor(F)))
            elif mode=='Dominio y rango':
                from sympy.calculus.util import continuous_domain,function_range
                d=continuous_domain(F,x,sp.S.Reals);show('Dominio real (donde la función está definida y es continua):',d)
                try:show('Rango real:',function_range(F,x,d))
                except Exception:st.warning('No se pudo determinar automáticamente el rango exacto.')
            else:
                G=parse(g);show('g(x):',G);show('Sustitución f(g(x)):',F.subs(x,G));show('Resultado simplificado:',sp.simplify(F.subs(x,G)))
        safe(solve_alg)
with tab[1]:
    st.subheader('Representación gráfica')
    f=st.text_input('Función a graficar',value='x^3-6*x^2+9*x+1',key='graph')
    c1,c2=st.columns(2)
    with c1:low=st.number_input('Desde x =',value=-2.,key='lo')
    with c2:high=st.number_input('Hasta x =',value=6.,key='hi')
    if st.button('Graficar e interpretar'):
        def plot():
            if low>=high:raise ValueError('El extremo izquierdo debe ser menor que el derecho.')
            F=parse(f);fn=sp.lambdify(x,F,modules=['numpy']);xs=np.linspace(low,high,900)
            with np.errstate(all='ignore'):
                yy=fn(xs);ys=np.broadcast_to(np.asarray(yy,dtype=float),xs.shape).copy()
            ys[~np.isfinite(ys)]=np.nan
            if np.isfinite(ys).sum()<2:raise ValueError('La función no tiene suficientes valores reales en el intervalo.')
            fig=go.Figure();fig.add_trace(go.Scatter(x=xs,y=ys,mode='lines',name='f(x)',connectgaps=False))
            fig.add_hline(y=0,line_color='gray');fig.add_vline(x=0,line_color='gray')
            fig.update_layout(xaxis_title='x',yaxis_title='f(x)',height=440)
            st.plotly_chart(fig,use_container_width=True)
            show('Intersección con eje y:',sp.simplify(F.subs(x,0)))
            roots=sp.solveset(F,x,domain=sp.Interval(low,high));show('Intersecciones con eje x en el intervalo:',roots)
            D=sp.diff(F,x);show('Derivada para estudiar crecimiento:',D)
            try:
                inc=sp.solve_univariate_inequality(D>0,x,relational=False);dec=sp.solve_univariate_inequality(D<0,x,relational=False)
                show('Creciente donde:',inc);show('Decreciente donde:',dec)
            except Exception:st.info('No se pudo determinar el crecimiento simbólicamente.')
        safe(plot)
with tab[2]:
    st.subheader('Límites')
    f=st.text_input('f(x)',value='(x^2-1)/(x-1)',key='limit')
    point=st.text_input('x tiende a (puedes usar oo o -oo)',value='1')
    direction=st.selectbox('Dirección',['Ambos lados','Por la izquierda','Por la derecha'])
    if st.button('Calcular límite'):
        def lim():
            F=parse(f);p=sp.oo if point.strip()=='oo' else -sp.oo if point.strip()=='-oo' else parse(point)
            if p.has(x):raise ValueError('El punto del límite debe ser constante.')
            show('Fórmula del límite:',sp.Limit(F,x,p,dir={'Ambos lados':'+-','Por la izquierda':'-','Por la derecha':'+'}[direction]))
            if p.is_finite:
                show('Sustitución directa (si está definida):',F.subs(x,p))
            fact=sp.cancel(F)
            if fact!=F:show('Simplificación algebraica:',fact)
            direction_code={'Ambos lados':'+-','Por la izquierda':'-','Por la derecha':'+'}[direction]
            answer=sp.limit(F,x,p,dir=direction_code);show('Resultado:',answer)
            if answer in [sp.nan,sp.zoo]:st.warning('El límite no tiene un valor finito determinado.')
        safe(lim)
with tab[3]:
    st.subheader('Derivadas')
    f=st.text_input('f(x)',value='x^3-6*x^2+9*x+1',key='der')
    order=st.selectbox('Orden de derivación',[1,2,3])
    if st.button('Derivar y verificar'):
        def der():
            F=parse(f);show('Función original:',F)
            for n in range(1,order+1):show(f'Derivada de orden {n}:',sp.diff(F,x,n))
            show('Verificación simbólica (debe dar 0):',sp.simplify(sp.diff(F,x,order)-sp.diff(F,x,order)))
            st.info('Reglas aplicadas: linealidad, potencia, producto, cociente o cadena, según corresponda.')
        safe(der)
with tab[4]:
    st.subheader('Integrales')
    f=st.text_input('Integrando f(x)',value='3*x^2+2*x',key='integ')
    kind=st.radio('Tipo',['Indefinida','Definida'],horizontal=True)
    if kind=='Definida':
        c1,c2=st.columns(2)
        with c1:left=st.text_input('Límite inferior a',value='0')
        with c2:right=st.text_input('Límite superior b',value='2')
    if st.button('Integrar'):
        def integ():
            F=parse(f);A=sp.integrate(F,x)
            if isinstance(A,sp.Integral):raise ValueError('No se encontró una primitiva elemental para este caso.')
            show('Paso 1: primitiva F(x):',A)
            if kind=='Indefinida':st.latex(sp.latex(A)+r'+C')
            else:
                aa=parse(left);bb=parse(right)
                if aa.has(x) or bb.has(x):raise ValueError('Los límites deben ser constantes.')
                show('Paso 2: teorema fundamental F(b)-F(a):',sp.simplify(A.subs(x,bb)-A.subs(x,aa)))
                show('Resultado de la integral definida:',sp.integrate(F,(x,aa,bb)))
            show('Verificación: derivar la primitiva:',sp.diff(A,x))
        safe(integ)
with tab[5]:
    st.subheader('Aplicaciones: extremos y razones de cambio')
    f=st.text_input('Función de la situación',value='x^3-6*x^2+9*x+1',key='app')
    t=st.text_input('Evaluar razón de cambio en x =',value='2')
    if st.button('Analizar función'):
        def applications():
            F=parse(f);D=sp.diff(F,x);DD=sp.diff(D,x)
            show('Función:',F);show('Primera derivada:',D);show('Segunda derivada:',DD)
            crit=sp.solveset(D,x,domain=sp.S.Reals);show('Puntos críticos (f’(x)=0):',crit)
            if isinstance(crit,sp.FiniteSet):
                for c in sorted(crit,key=lambda v:float(sp.N(v))):
                    val=sp.simplify(F.subs(x,c));second=sp.simplify(DD.subs(x,c))
                    kind='Mínimo relativo' if second.is_positive else 'Máximo relativo' if second.is_negative else 'Prueba inconclusa; analizar cambio de signo de f’'
                    st.write(f'**x = {c}; f(x) = {val}: {kind}.**')
                    show('Sustitución en segunda derivada:',second)
            v=parse(t)
            if v.has(x):raise ValueError('El punto de evaluación debe ser constante.')
            show('Razón de cambio instantánea f’(x) evaluada:',sp.simplify(D.subs(x,v)))
            st.caption('Interpretación: la derivada representa la variación instantánea de la magnitud modelada respecto de x.')
        safe(applications)

EXAMPLES=[('Ecuación','x^2-5*x+6=0','x = 2 y x = 3'),('Factorización','x^2-9','(x-3)(x+3)'),('Dominio','1/(x-2)','Todos los reales excepto 2'),('Composición','f(x)=x^2, g(x)=x+1','(x+1)^2'),('Gráfica','x^2-4','Corta el eje x en -2 y 2'),('Límite','(x^2-1)/(x-1), x→1','2'),('Derivada','x^3','3x^2'),('Integral indefinida','2*x','x^2+C'),('Integral definida','∫₀² x dx','2'),('Extremos','x^3-6*x^2+9*x+1','Máximo (1,5), mínimo (3,1)')]
with tab[6]:
    st.subheader('10 ejercicios de ejemplo')
    for i,(typ,problem,answer) in enumerate(EXAMPLES,1):
        with st.expander(f'{i}. {typ}: {problem}'):
            st.write('**Resultado esperado:**',answer)
            st.caption('Utiliza el módulo correspondiente para ver los pasos calculados con tus propios datos.')
    st.divider();st.subheader('Práctica con retroalimentación')
    if 'exercise' not in st.session_state:st.session_state.exercise=(2,3,'der')
    if st.button('Generar nuevo ejercicio'):
        a=random.randint(2,8);b=random.randint(1,6);k=random.choice(['der','int','eval'])
        st.session_state.exercise=(a,b,k)
    a,b,k=st.session_state.exercise
    if k=='der':question=f'Deriva f(x)={a}*x^{b}';expected=a*b*x**(b-1)
    elif k=='int':question=f'Integra f(x)={a}*x^{b} (sin escribir +C)';expected=sp.integrate(a*x**b,x)
    else:question=f'Evalúa f(x)={a}*x+{b} en x=2';expected=sp.Integer(2*a+b)
    st.write('**Ejercicio:**',question)
    response=st.text_input('Tu respuesta (usa x^2 para potencias)',key='answer')
    if st.button('Comprobar respuesta'):
        def check():
            actual=parse(response)
            if sp.simplify(actual-expected)==0:st.success('¡Correcto! Tu respuesta es equivalente al resultado esperado.')
            else:st.error('Aún no es correcto. Revisa la regla y vuelve a intentarlo.')
            show('Solución explicada:',expected)
            if k=='der':st.write(f'Regla de la potencia: d(a·x^n)/dx = a·n·x^(n−1). Aquí a={a} y n={b}.')
            elif k=='int':st.write(f'Regla de integración: ∫a·x^n dx = a·x^(n+1)/(n+1)+C. Aquí a={a} y n={b}.')
            else:st.write(f'Sustituye x=2: {a}·2+{b}={2*a+b}.')
        safe(check)

st.divider()

st.markdown("""
### Información del proyecto

**Universidad Mariano Gálvez de Guatemala**

**Proyecto:** MathGenius UMG

**Integrantes:**
- Richard Alexander Flores Gramajo
- Mario David Guerra Sazo

**Sección:** B

**Asignatura:** Cálculo y Precálculo
""")

st.caption('Advertencia: algunas expresiones avanzadas pueden requerir métodos no implementados. Revisa siempre el dominio y las restricciones.')
